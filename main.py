#!/usr/bin/env python3
"""每日选股分析报告主入口"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher
from modules.data_processor import DataProcessor
from modules.stock_analyzer import StockAnalyzer
from modules.ai_analyzer import AIAnalyzer
from modules.report_generator import ReportGenerator
from modules.converter import Converter
from modules.email_sender import EmailSender
from modules.chanlun import ChanAnalyzer
from utils.logger import setup_logger
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
    """主函数"""
    logger = setup_logger()
    logger.info("开始执行每日选股分析任务")
    
    try:
        # 1. 获取时间信息
        logger.info("第一步：获取权威时间")
        time_service = TimeService()
        time_info = time_service.get_time_info()
        
        # 2. 获取市场数据
        logger.info("第二步：获取市场数据")
        data_fetcher = DataFetcher()
        market_data = data_fetcher.fetch_all_data(time_info)
        
        # 3. 处理数据
        logger.info("第三步：处理数据")
        data_processor = DataProcessor()
        processed_data = data_processor.process_data(market_data)
        
        # 4. AI新闻筛选分析（先做，因为选股需要用到）
        logger.info("第四步：AI新闻筛选分析")
        ai_analyzer = AIAnalyzer()
        news_analysis = ai_analyzer.select_and_analyze_all_news(market_data.get('news', {}).get('all_news', []))
        
        # 5. 基于缠论理论的AI选股
        logger.info("第五步：基于缠论理论的AI选股")
        stock_analyzer = StockAnalyzer()
        
        # 获取热门股票列表（用于缠论分析）
        hot_stocks = data_fetcher.fetch_hot_stocks(limit=50)
        
        # 对这些股票进行缠论技术分析
        chan_analyzer = ChanAnalyzer()
        chanlun_analysis = []
        
        def analyze_single_stock(stock):
            code = stock.get('code', '')
            if code:
                try:
                    import time
                    time.sleep(0.5)  # 添加延迟避免请求过快
                    chan_result = chan_analyzer.analyze(code)
                    stock['daily'] = chan_result.get('daily', {})
                    stock['60min'] = chan_result.get('60min', {})
                    stock['15min'] = chan_result.get('15min', {})
                    return stock
                except Exception as e:
                    print(f'缠论分析 {code} 失败: {e}')
            return None
        
        # 使用线程池并发分析，降低并发数避免被封
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(analyze_single_stock, stock): stock for stock in hot_stocks}
            for future in as_completed(futures, timeout=300):  # 300秒总超时
                try:
                    result = future.result(timeout=60)  # 单个任务60秒超时
                    if result:
                        chanlun_analysis.append(result)
                except Exception as e:
                    print(f'缠论分析超时或失败: {e}')
        
        print(f'完成缠论分析的股票数量: {len(chanlun_analysis)}')
        
        # 使用AI基于缠论分析结果选股
        sectors = market_data.get('sectors', [])
        ai_selection = ai_analyzer.ai_select_stocks_chanlun(
            market_data,
            chanlun_analysis,
            sectors,
            news_analysis
        )

        # 如果缠论选股为空，使用龙虎榜数据的AI选股作为回退
        if not ai_selection.get('selected_codes'):
            print('缠论选股为空，尝试使用龙虎榜数据AI选股...')
            lhb_data = market_data.get('lhb', {}).get('top_buy', [])
            if lhb_data:
                ai_selection = ai_analyzer.ai_select_stocks(market_data, lhb_data, sectors)
                print(f'龙虎榜AI选股: {len(ai_selection.get("selected_codes", []))}只')

            # 如果仍然为空，直接使用龙虎榜前5只
            if not ai_selection.get('selected_codes') and lhb_data:
                ai_selection = {
                    'selected_codes': [s.get('code', '') for s in lhb_data[:5]],
                    'ai_reasons': [{'code': s.get('code', ''), 'name': s.get('name', ''), 'reason': f"龙虎榜净买入{s.get('net_buy', 0):.0f}万"} for s in lhb_data[:5]],
                    'market_logic': '基于龙虎榜资金净买入筛选'
                }
                print(f'使用龙虎榜前{len(ai_selection["selected_codes"])}只股票作为候选')
        
        # 准备增强数据
        enhanced_data = processed_data.copy()
        enhanced_data['ai_selected_codes'] = ai_selection.get('selected_codes', [])
        enhanced_data['ai_stock_reasons'] = ai_selection.get('ai_reasons', [])
        enhanced_data['ai_market_logic'] = ai_selection.get('market_logic', '')
        enhanced_data['chanlun_analysis'] = chanlun_analysis
        enhanced_data['hot_stocks'] = hot_stocks  # 传递热门股票用于补充
        
        # 合并AI新闻筛选结果
        enhanced_data['geopolitics_selected'] = news_analysis.get('geopolitics', {}).get('selected_news', [])
        enhanced_data['geopolitics_analysis'] = news_analysis.get('geopolitics', {}).get('analysis', '')
        enhanced_data['macro_economy_selected'] = news_analysis.get('macro_economy', {}).get('selected_news', [])
        enhanced_data['macro_economy_analysis'] = news_analysis.get('macro_economy', {}).get('analysis', '')
        enhanced_data['government_policy_selected'] = news_analysis.get('government_policy', {}).get('selected_news', [])
        enhanced_data['government_policy_analysis'] = news_analysis.get('government_policy', {}).get('analysis', '')
        
        # 5.5 板块驱动因素AI分析
        logger.info("第五步半：板块驱动因素AI分析")
        sectors_data = enhanced_data.get('sectors', [])
        for i, sector in enumerate(sectors_data[:10]):
            if not sector.get('reason'):
                try:
                    reason = ai_analyzer.analyze_sector_driver(sector.get('name', ''), sector.get('pct', 0))
                    enhanced_data['sectors'][i]['reason'] = reason
                except Exception as e:
                    print(f'板块分析失败 {sector.get("name", "")}: {e}')
        
        # 5.6 美股和商品AI分析
        logger.info("第五步六：美股和商品AI分析")
        # 美股要点
        try:
            us_summary = ai_analyzer.analyze_us_stock(enhanced_data.get('us_stock', {}))
            enhanced_data['us_stock']['summary'] = us_summary
        except Exception as e:
            print(f'美股AI分析失败: {e}')

        # 美股备注
        try:
            us_notes = ai_analyzer.analyze_us_stock_notes(enhanced_data.get('us_stock', {}))
            if us_notes.get('djia'):
                enhanced_data['us_stock']['djia']['note'] = us_notes['djia']
            if us_notes.get('nasdaq'):
                enhanced_data['us_stock']['nasdaq']['note'] = us_notes['nasdaq']
            if us_notes.get('sp500'):
                enhanced_data['us_stock']['sp500']['note'] = us_notes['sp500']
        except Exception as e:
            print(f'美股备注AI分析失败: {e}')

        # 商品要点
        commodity_data = enhanced_data.get('commodity', {})
        try:
            commodity_summary = ai_analyzer.analyze_commodity(commodity_data)
            enhanced_data['commodity']['summary'] = commodity_summary
        except Exception as e:
            print(f'商品AI分析失败: {e}')

        # 单个商品补充
        for key in ['gold', 'wti', 'brent']:
            if commodity_data.get(key, {}).get('need_ai'):
                try:
                    ai_commodity_summary = ai_analyzer.analyze_commodity({key: commodity_data[key]})
                    enhanced_data['commodity'][key]['summary'] = ai_commodity_summary
                except Exception as e:
                    print(f'商品AI分析失败 {key}: {e}')
        
        # 6. 分析股票（使用AI选择的股票）
        logger.info("第六步：分析股票")
        analysis_results = stock_analyzer.analyze_stocks(enhanced_data)
        
        # 合并AI增强结果到最终分析
        analysis_results['ai_stock_reasons'] = enhanced_data.get('ai_stock_reasons', [])
        analysis_results['ai_selected_codes'] = enhanced_data.get('ai_selected_codes', [])
        analysis_results['ai_market_logic'] = enhanced_data.get('ai_market_logic', '')
        analysis_results['chanlun_analysis'] = enhanced_data.get('chanlun_analysis', [])
        
        # 合并AI新闻筛选结果
        analysis_results['geopolitics_selected'] = enhanced_data.get('geopolitics_selected', [])
        analysis_results['geopolitics_analysis'] = enhanced_data.get('geopolitics_analysis', '')
        analysis_results['macro_economy_selected'] = enhanced_data.get('macro_economy_selected', [])
        analysis_results['macro_economy_analysis'] = enhanced_data.get('macro_economy_analysis', '')
        analysis_results['government_policy_selected'] = enhanced_data.get('government_policy_selected', [])
        analysis_results['government_policy_analysis'] = enhanced_data.get('government_policy_analysis', '')
        
        # 7. 生成报告
        logger.info("第七步：生成报告")
        report_generator = ReportGenerator()
        report_path = report_generator.generate_report(analysis_results, time_info)
        
        # 8. 转换为PDF
        logger.info("第八步：转换为PDF")
        converter = Converter()
        pdf_path = converter.convert_to_pdf(report_path)

        # 9. 发送邮件
        logger.info("第九步：发送邮件")
        email_sender = EmailSender()
        email_sender.send_email(report_path, pdf_path, time_info)
        
        logger.info("每日选股分析任务完成")
        
    except Exception as e:
        logger.error(f"执行过程中发生错误: {e}")
        # 尝试发送失败通知邮件
        try:
            email_sender = EmailSender()
            if email_sender.sender_email and email_sender.sender_password:
                import smtplib
                from email.mime.text import MIMEText
                msg = MIMEText(f'每日选股报告生成失败\n\n错误信息: {str(e)}\n\n请检查系统日志。', 'plain', 'utf-8')
                msg['Subject'] = '每日选股报告 - 生成失败'
                msg['From'] = email_sender.sender_email
                msg['To'] = ','.join(email_sender.receiver_emails)
                server = smtplib.SMTP(email_sender.smtp_server, email_sender.smtp_port)
                server.starttls()
                server.login(email_sender.sender_email, email_sender.sender_password)
                server.sendmail(email_sender.sender_email, email_sender.receiver_emails, msg.as_string())
                server.quit()
                logger.info("已发送失败通知邮件")
        except Exception as email_error:
            logger.error(f"发送失败通知邮件出错: {email_error}")
        raise


if __name__ == "__main__":
    main()
