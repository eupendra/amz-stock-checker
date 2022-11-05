import logging
import smtplib
import webbrowser
import os

import scraper_helper as helper
import scrapy

logging.basicConfig(filename='amz.log',level=logging.INFO)

asins = ['B07NF6J8N5']
base_url = 'https://www.amazon.in/gp/product/{}/ref=ox_sc_saved_image_3?smid=&th=1'


class AmazonStockSpider(scrapy.Spider):
    name = 'stock'
    custom_settings = {
        'LOG_LEVEL':'INFO', 
        'LOG_FILE':'amz.log'
        }
    def start_requests(self):
        headers = helper.get_dict('''
                        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                        accept-encoding: gzip, deflate, br
                        accept-language: en-US,en;q=0.9
                        cache-control: no-cache
                        cookie: ubid-acbin=260-9826739-0297225; sst-acbin=Sst1|PQGE1A2dyfLxDIkw22MXQe6uCZpZyWD5evlcZTprgH70kns6Rkyzg1Nd8u64xu0oScR3-77LQMNxcMPRJW4G3mQ72v2yVz_qoC5QvYuTdVW_N1mvTlYdLo-7UWlg4LrjE7figKcJOMEgJa914w4dIiVDdObOhoj6-ds1JVtiE9DKtyNb5cC4m8CZyrAWWco_iqIZDC81zYzPP8THA5c_Y7U-TfEepGbX30ZpB4Lbn-4K-l7vvqPg7fjUKEpqcK2F2or42BEewkSZfodcFgyiOYYO-esdSvCgFXTixtsUaz-lp5A; i18n-prefs=INR; x-acbin="xF?yVZzOkofNkgY7z2QmXjSOP3ZtEJ7i"; at-acbin=Atza|IwEBIH_LvFj51RSgAsMjGqhgYaTLgXhjHqQEhHScylxQ4E74EngQms2oUaHpCYr80eXZIGA3su1C8Ev6JxMQTmr4utD3gFDoy8FRYuEbx1ZKA9UJR3PU6S1Pz5fSvgzWNq1Hkx7DBuxwT727JQbpXjwdlQwNIXxaqgRP8j8ea6VUT8aTtf0D9YiKXAB70LNdCo_ejZ3bK1H12DQwOgA-jtSCm3aU6_N6tcSvt76_B7wduRZdSw; sess-at-acbin="tZjs97MeL326iEZSw0dSOKudaESeHr7us6H1x+cAzLA="; lc-acbin=en_IN; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiYTY2NzQ0Iiwia2V5IjoiUHZlVFlKdDQ3NU95eG03WDdrYUd0SE5KdGJic2hrbC9wckpwc0NaUk5Hc0VaRVFjeVRnTDkzV0p3SVZ3QnFqdE1jNXlib09HNnRROCs0ZTExdE9MTGFxdjhRdXdQTGFMZFc1c3RQdDBuNHBwbkk4dGJhc0Y3QzNGUEFLcDZKTGo0WEVYem9nYW1Jbm1OMCtFUkt3V2gvOGk2dGl4QlViQW9MVjZkMHVNazVQNmR4Uit3NkFabzBhMGRpY053TVpaMmtvdnNiQU9tZUlSY3BMcG9YVXl2dmdhQlQwYVk4WTRxa3dSTnIyMUxIaUFHSDhYbGtxbUhBQm01RUQyY3UzcHFKQy9Cb0RhY0tKSlhUVGxZbHlQS3BYaW1MV0E0MVdYcmZJaEZUblVlSFRESERuK0pwbTRjRE1PcVBYeTAvMzk3Q2lCOGYzcTRtY3A2TkpPOWtJL3lRPT0ifQ==; session-id=261-5695877-3259325; s_fid=57760D9E746E8445-02DAC1923E93CB23; s_cc=true; s_sq=%5B%5BB%5D%5D; _rails-root_session=YmVVUTVqSEhsWWRBdVp1S1RHVWtCY2FQTHJsclAycWF3NVU2MXFoY2d0aEx1SUFPSFNtajJwOWZQaEo1WURxUldxYzFiaTZsM1IvUUNzRENpbmF1cEJSb2R6U0dBUVNuT2dCVE9zU2psSnlFQWZCVFJDaUFiWWtNWjh4V0ZoNHVZT25FdE5ZN0FybzJPTGhSdFpDNXkzeWRtU25KWmc2VGFqV2N2Yll6am9iS3lsUGhNckdzMkRpNzRKdlFVVDdwLS1MWEFxYzJnbVNyQUlBUG5KQWI5dW53PT0%3D--02e6b4ca08fa1b97465b94332d1d4e6b1690cf8f; csm-hit=tb:26NNJKC6BNWGKTQGB2SJ+sa-Y8PSKQNDB1HSBR4SN79A-N8Q89XV7B3Y4Y1QD3XF4|1664014102214&t:1664014102214&adb:adblk_no; session-token="wNl3l6W2ZiEa1g8V4CR3jgapY58nfsF6Xpb1+AKQlZf/tZyMU5kp/4STCx1CBp4d/A9qjDCwlkbB/rc48VEivgX/oz7iDskgdktUio/dokqHlwTBWQSGog5RvnGELa9SW1PqRLd7yLZRs7zGS8OqdXttqAShFtdjf8G4OeyAFlWnHKSae+xewE8m9TAoV++la8YdYbKx9mn32PPS6LNIdQolpO/FQ2R1UqKdPmNpBAqh4obySFfNrQ=="; session-id-time=2082787201l
                        device-memory: 8
                        downlink: 10
                        dpr: 2
                        ect: 4g
                        pragma: no-cache
                        referer: https://www.amazon.in/gp/cart/view.html?ref_=nav_cart
                        rtt: 150
                        sec-ch-device-memory: 8
                        sec-ch-dpr: 2
                        sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"
                        sec-ch-ua-mobile: ?0
                        sec-ch-ua-platform: "macOS"
                        sec-ch-viewport-width: 3008
                        sec-fetch-dest: document
                        sec-fetch-mode: navigate
                        sec-fetch-site: same-origin
                        sec-fetch-user: ?1
                        service-worker-navigation-preload: true
                        upgrade-insecure-requests: 1
                        user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
                        viewport-width: 3008
                                  ''')
        for asin in asins:
            yield scrapy.Request(base_url.format(asin),
                                 headers=headers,
                                 cb_kwargs={
                                     'asin': asin
            })

    def parse(self, response, asin):
        if response.css('#outOfStock').get():
            self.logger.warning(f'{asin} not in stock. Checked {response.url}')
            return
        else:
                                 
            product = response.css('#productTitle::text').get()
            product = product.encode('utf-8').decode().strip()
            body = f'{product}\n{response.url}'
            subject = f'{product} is in stock!'
            self.logger.info(subject)
            send_mail(subject, body)


def send_mail(subject, body):
    USER = os.environ.get('MAIL_USER')
    PASS = os.environ.get('MAIL_PASS')
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(USER, PASS)
            subject_and_message = f"Subject:{subject}\n\n{body}"
            smtp.sendmail(USER, USER, subject_and_message)
            logging.info('Mail sent.')
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')


if __name__ =='__main__':
    helper.run_spider(AmazonStockSpider)
