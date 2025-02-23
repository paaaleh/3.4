document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById('loader');
    const itemsContainer = document.getElementById('items');

    const renderCurrencyRates = (currencyData) => {
        itemsContainer.innerHTML = '';
        Object.values(currencyData).forEach(currency => {
            const currencyElement = createCurrencyElement(currency);
            itemsContainer.appendChild(currencyElement);
        });
    };

    const createCurrencyElement = (currency) => {
        const currencyElement = document.createElement('div');
        currencyElement.classList.add('item');
        currencyElement.innerHTML = `
            <div class="item__code">${currency.CharCode}</div>
            <div class="item__value">${currency.Value.toFixed(2)}</div>
            <div class="item__currency">руб.</div>
        `;
        return currencyElement;
    };

    const fetchCurrencyRates = async () => {
        try {
            const response = await fetch('https://students.netoservices.ru/nestjs-backend/slow-get-courses');
            const data = await response.json();
            const currencyData = data.response.Valute;
            localStorage.setItem('currencyRates', JSON.stringify(currencyData));
            renderCurrencyRates(currencyData);
        } catch (error) {
            console.error('Ошибка при загрузке данных:', error);
        } finally {
            loader.classList.remove('loader_active');
        }
    };

    const loadCachedData = () => {
        const cachedData = localStorage.getItem('currencyRates');
        if (cachedData) {
            const currencyData = JSON.parse(cachedData);
            renderCurrencyRates(currencyData);
        }
    };

    loadCachedData();
    fetchCurrencyRates();
});
