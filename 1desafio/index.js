const pup = require('puppeteer');
const fs = require('fs');
const url = "https://www.adidas.com.br/calcados";

let numPage = 1;
const todosDados = [];

(async () => {
  const browser = await pup.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(url, { waitUntil: 'domcontentloaded' });

  await page.waitForSelector('#glass-gdpr-default-consent-accept-button', { timeout: 10000 });
  await page.click('#glass-gdpr-default-consent-accept-button');

  while (true) {
    console.log(`Página ${numPage}`);

    await page.waitForSelector('.product-card_product-card-content___bjeq', { timeout: 10000 });

    const dados = await page.$$eval('.product-card_product-card-content___bjeq', (produtos) => {
      return produtos.map((produto) => {
        const nome = produto.querySelector('.product-card-description_name__xHvJ2')?.innerText || null;
        const preco = produto.querySelector('._priceComponent_1dbqy_14')?.innerText || null;
        const categoria = produto.querySelector('.product-card-description_info__z_CcT')?.innerText || null;
        const imgUrl = produto.querySelector('img')?.src || null;
        return { nome, preco, categoria, imgUrl };
      });
    });

    console.log(`→ ${dados.length} produtos encontrados`);
    todosDados.push(...dados);

    // Lógica para fechar modal ADIDAS CLUB
    const btnCloseModal = await page.$('#gl-modal__close-mf-account-portal');
    if (btnCloseModal) {
      await btnCloseModal.click();
    }

    // Lógica botão PRÓXIMO
    const btnProximo = await page.$('a[data-testid="pagination-next-button"]');

    if (!btnProximo) {
      console.log('Última página alcançada');
      break;
    }

    const currentUrl = page.url();
    await Promise.all([
      btnProximo.click(),
      page.waitForFunction(
        (oldUrl) => window.location.href !== oldUrl,
        {},
        currentUrl
      )
    ]);

    numPage++;
  }

  //Lógica para criar o arquivo com as informações dos tênis
  fs.writeFileSync('produtos_adidas.json', JSON.stringify(todosDados, null, 2), 'utf-8');
  console.log('Dados salvos em: produtos_adidas.json');

  await browser.close();
})();
