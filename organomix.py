from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Item
from scrapy import Field
from logging import INFO
import json


# O crawling exige que facamos um "contrato" do item que iremos extrair
class Product(Item):
    name = Field()
    price = Field()
    image = Field()


class Organomix(CrawlSpider):
    name = 'organomix'
    # Com essa variavel o crawler nao conseguirá sair do dominio do site
    # por mais que alguma regra de pattern esteja furada
    allowed_domains = ['organomix.com.br']
    # Primeiramente testei com o start no menu principal. Funciona mas precisa rever a regra para perfomar melhor
    start_urls = ['https://www.organomix.com.br']

    # Daí decidi por, enquanto não azeito as regras, comecar o crawling pelas categorias fixas do site
    # start_urls = [
    #     'https://www.organomix.com.br/horta---pomar',
    #     'https://www.organomix.com.br/ovos---laticinios',
    #     'https://www.organomix.com.br/carnes---pescados',
    #     'https://www.organomix.com.br/bebidas',
    #     'https://www.organomix.com.br/para-a-despensa',
    #     'https://www.organomix.com.br/para-a-geladeira',
    #     'https://www.organomix.com.br/para-a-casa',
    #     'https://www.organomix.com.br/linha-pet'
    # ]

    rules = [
        # Regra simples para entrar na subsessão (url contém =O). Pode melhorar
        Rule(LinkExtractor(allow=('^.*O=.*?$',), )),
        # Regra para item parseado
        Rule(LinkExtractor(allow=('^.*?/p$',)), callback='parse_item'),
    ]

    def parse_item(self, response):
        self.log('Parsing url-> {}'.format(response.url), INFO)
        product = Product()
        product['name'] = response.xpath('//h1[@id="productName"]/div/text()').extract_first()
        # Parseando para float e assim facilitar o cálculo (Uma ou outra página sem esse padrão)
        # No futuro podemos colocar essas transformacoes em um pipeline
        product['price'] = float(response.xpath('//div[@id="productPrice"]//strong[@class="skuBestPrice"]/text()')
                                 .re(r'R\$\s*(\d+,\d+)')[0]
                                 .replace(',', '.'))
        product['image'] = response.xpath('//div[@id="image"]/a/@href').extract_first()
        return product


# Pipeline para escrever o item num arquivo json (Poderia ser no mongo/rabbit ou qualquer outra merda)
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('{}.json'.format(spider.name), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
