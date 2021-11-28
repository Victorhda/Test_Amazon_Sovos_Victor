from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestAmazon:

    def test_products(self):

        """Variaveis que serão usadas posteriormente"""
        all_values = []
        total_value = 0
        x = 0
        budget_per_item = 300.00

        """Driver de escolha = Chrome"""
        driver = webdriver.Chrome()

        """Códigos de produto únicos chamados asin
        a minha ideia inicial era implementar a api 
        de asins da amazon para pegar asins aleatórios e adicionar mais
        produtos ao teste, porém eu não tive tempo"""

        asin_set = ['B08XY4KCZ3', 'B09HGT8CC9', 'B07PDFBJZD']

        """Percorrer lista de asin e abrir a pagina de cada um"""
        for i in range(len(asin_set)):
            """Obrigar o 'for' a continuar até o final da lista de Asins antes de retornar todos os valores"""
            x = x + 1
            if x > i:

                """Url padrão recebe asin único"""
                url = 'https://www.amazon.com.br/gp/product/{}'.format(asin_set[i])

                """Driver recebe url do produto e fica em tela cheia"""
                driver.get(url)
                driver.maximize_window()

                """Pausa obrigatória para dar tempo de carregar o produto"""
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//span[@id="productTitle"]'
                                                                                  )))
                """Verificar se o produto está disponível para compra"""
                avaliability = driver.find_element(By.XPATH, '//*[@id="availability"]/span').text
                assert avaliability == 'Em estoque.'

                """Verifica se a quantidade a ser adicionada do produto é somente um"""
                quantity = driver.find_element(By.ID, 'quantity').get_attribute('value')
                assert quantity == '1'

                """Recebe o valor do produto em string, transforma em float, e verifica se ele respeita o valora máximo de
                R$300"""
                value = driver.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]//span[2]').text
                value = value.replace('R$', '')
                value = value.replace('.', '')
                value = value.replace(',', '.')
                value = float(value)

                if value <= budget_per_item:
                    all_values.append(value)

                    """Adiciona o produto ao carrinho"""
                    add_to_cart = driver.find_element(By.ID, 'add-to-cart-button')
                    add_to_cart.click()

                else:
                    """Caso o produto não respeite o limite imposto, será tirada uma screenshot de qual produto 
                    não pode ser adicionado"""
                    driver.maximize_window()
                    driver.save_screenshot("Este produto não respeitou o limite imposto.png")
                    continue

            else:
                return all_values

        """Uma exception será levantada caso nenhum dos produtos avaliados tenha respeitado o limite imposto"""
        if all_values == 0:
            raise Exception("Sorry, no products under R$300,00 were found")

        """Neste passo, o carrinho é aberto."""
        open_cart = driver.find_element(By.ID, 'nav-cart-count-container')
        open_cart.click()

        """Todos os valores adicionados a lista são somados para que seja calculador o valor final"""
        for i in range(len(all_values)):
            total_value = total_value + all_values[i]

        """O valor final fornecido pela amazon é refatorado e salvo como float dentro de uma variável"""

        WebDriverWait(driver, 2).until(
        ec.visibility_of_element_located((By.XPATH, '//*[@id="sc-subtotal-amount-buybox"]/span')))
        final_value = driver.find_element(By.XPATH, '//*[@id="sc-subtotal-amount-buybox"]/span').text
        final_value = final_value.replace('R$ ', '')
        final_value = final_value.replace('.', '')
        final_value = final_value.replace(',', '.')
        final_value = float(final_value)

        """O valor final fornecido pela amazon é comparado com o valor que o teste calculou baseado na lista"""
        assert total_value == final_value

        """É tirada uma screenshot do carrinho caso o assert seja positivo, e o nome dessa screenshot contém o valor
        final já validado com uma mensagem"""
        driver.maximize_window()
        driver.save_screenshot("Your purchase's value is {}.png".format(total_value))
