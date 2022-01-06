# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import xlsxwriter
import os, xlrd, datetime, csv
from collections import OrderedDict
from datetime import timedelta, datetime

class InmetGovBrPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):

        f2 = open('inmet_gov_br/spiders/ids.csv')
        csv_items = csv.DictReader(f2)
        for i, row in enumerate(csv_items):
            spider.ids.append(row['id'])
        f2.close()

        f1 = open('input_data/input.csv')
        csv_items1 = csv.DictReader(f1)
        for i, row in enumerate(csv_items1):
            spider.start_date = row['startdate']
            spider.end_date = row['enddate']
            break
        f1.close()

        file_path = ''
        if spider.name == "inmet_gov_br":
            file_path = 'output/result1.xlsx'
        elif spider.name == "inmet_gov_br_temp":
            file_path = 'output/result_temp.xlsx'
        spider.file_path = file_path
        if not os.path.isfile(file_path):
            print('not existing')

            workbook = xlsxwriter.Workbook(file_path)
            if spider.name == "inmet_gov_br":
                worksheet = workbook.add_worksheet('Rain Fall')
            elif spider.name == "inmet_gov_br_temp":
                worksheet = workbook.add_worksheet('Temp Comp')

            start_date = datetime.strptime('Jan 1 2005', '%b %d %Y')
            nn = 1
            for single_date in (start_date + timedelta(n) for n in range(5490)):
                # print(single_date.strftime("%d/%m/%Y"))
                spider.all_date_data.append(single_date.strftime("%d/%m/%Y"))
                worksheet.write(nn, 0, single_date.strftime("%d/%m/%Y"))#write station id on first row
                nn += 1

            # for i, id_vavl in enumerate(spider.ids):
            #     worksheet.write(0, i + 1, str(id_vavl))#write station id on first row
            workbook.close()
        else:
            book = xlrd.open_workbook(file_path)
            sh = book.sheet_by_index(0)

            spider.now_row_count = sh.nrows
            if spider.now_row_count == 0:
                spider.now_row_count = 1

            # spider.now_row_count += 1

            for row_index in range(sh.nrows):
                if row_index == 0:
                    continue
                a1 = sh.cell_value(rowx=row_index, colx=0)
                if not isinstance(a1, str):
                    a1_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(a1, book.datemode))
                    date_str = a1_as_datetime.strftime("%d/%m/%Y")
                    spider.all_date_data.append(date_str)
                else:
                    spider.all_date_data.append(a1)

            for col_index in range(sh.ncols):
                if col_index == 0:
                    continue
                a1 = sh.cell_value(rowx=0, colx=col_index)
                if isinstance(a1, float) or isinstance(a1, int):
                    a1 = str(int(a1))

                spider.all_stations.append(a1)
            book.release_resources()
            del book
            print('existing')

    def spider_closed(self, spider):
        # spider.workbook_to_write.close()
        spider.wb.save(spider.file_path)
        pass


    def process_item(self, item, spider):
        return item
