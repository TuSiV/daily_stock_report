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
from utils.logger import setup_logger


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
        
        # 4. 分析股票
        logger.info("第四步：分析股票")
        stock_analyzer = StockAnalyzer()
        analysis_results = stock_analyzer.analyze_stocks(processed_data)
        
        # 5. AI增强分析
        logger.info("第五步：AI增强分析")
        ai_analyzer = AIAnalyzer()
        analysis_results = ai_analyzer.enhance_report(analysis_results)
        
        # 6. 生成报告
        logger.info("第六步：生成报告")
        report_generator = ReportGenerator()
        report_path = report_generator.generate_report(analysis_results, time_info)
        
        # 7. 转换为PNG和PDF
        logger.info("第七步：转换为PNG和PDF")
        converter = Converter()
        png_path, pdf_path = converter.convert_to_png_pdf(report_path)
        
        # 8. 发送邮件
        logger.info("第八步：发送邮件")
        email_sender = EmailSender()
        email_sender.send_email(report_path, png_path, pdf_path, time_info)
        
        logger.info("每日选股分析任务完成")
        
    except Exception as e:
        logger.error(f"执行过程中发生错误: {e}")
        raise


if __name__ == "__main__":
    main()
