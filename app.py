if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from organomix import Organomix

    # Configurando o Crawler
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # Nível máximo de crawling considerando que os start_urls são diretamente as categorias do supermercado
        'DEPTH_LIMIT': 3,
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': {
            # Esse número é a prioridade de execucao do pipeline em questao, quanto menor será executado primeiro.
            'organomix.JsonWriterPipeline': 1
        }
    })

    # É hora do show!
    process.crawl(Organomix)
    process.start()
