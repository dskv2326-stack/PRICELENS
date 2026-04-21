const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const searchBtn = document.querySelector('.search-btn');

function renderSearchResults(items) {
    if (!searchResults) return;

    if (!items.length) {
        searchResults.innerHTML = '<div class="search-row"><span>No products found</span></div>';
        return;
    }

    searchResults.innerHTML = items
        .slice(0, 8)
        .map(
            (item) => `
                <div class="search-row">
                    <div>
                        <strong>${item.name}</strong>
                        <div>\u20B9${Number(item.cheapest_price).toFixed(2)} on ${item.cheapest_platform}</div>
                    </div>
                    <a href="/product/${item.category}/${item.id}">View</a>
                </div>
            `
        )
        .join('');
}


let debounceTimer;
async function runSearch(query) {
    if (!query) {
        if (searchResults) searchResults.innerHTML = '';
        return;
    }
    try {
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        renderSearchResults(data);
    } catch (error) {
        if (searchResults) {
            searchResults.innerHTML = '<div class="search-row"><span>Search unavailable</span></div>';
        }
    }
}

if (searchInput) {
    searchInput.addEventListener('input', (event) => {
        const query = event.target.value.trim();
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => runSearch(query), 250);
    });
}

if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', () => runSearch(searchInput.value.trim()));
}

const compareModal = document.getElementById('compare-modal');
const compareList = document.getElementById('compare-list');
const compareTitle = document.getElementById('compare-title');
const compareMeta = document.getElementById('compare-meta');
const compareImage = document.getElementById('compare-image');

const PLATFORM_URLS = {
    Blinkit: 'https://www.blinkit.com',
    Zepto: 'https://www.zepto.com',
    Instamart: 'https://www.swiggy.com/instamart',
    Ajio: 'https://www.ajio.com',
    Myntra: 'https://www.myntra.com',
    Amazon: 'https://www.amazon.in',
    Flipkart: 'https://www.flipkart.com',
};

function getPlatformUrl(platform) {
    if (!platform) return null;
    return PLATFORM_URLS[platform] || null;
}

const CARD_REFRESH_INTERVAL_MS = 10000;

async function refreshCardPrices() {
    const cards = Array.from(document.querySelectorAll('.catalog-card[data-product-id]'));
    if (!cards.length) return;

    const ids = cards.map((card) => {
        const id = card.dataset.productId;
        const cat = card.dataset.productCategory;
        return id && cat ? `${cat}:${id}` : null;
    }).filter(Boolean);
    if (!ids.length) return;

    try {
        const response = await fetch(`/api/products/prices?items=${encodeURIComponent(ids.join(','))}`, { cache: 'no-store' });
        if (!response.ok) return;
        const payload = await response.json();
        const prices = payload.prices || {};

        cards.forEach((card) => {
            const id = card.dataset.productId;
            const info = prices[`${card.dataset.productCategory}:${id}`];
            if (!info) return;

            const amountEl = card.querySelector('.catalog-amount');
            const platformEl = card.querySelector('.catalog-platform');
            const pillEl = card.querySelector('.catalog-pill');

            if (amountEl) amountEl.textContent = `₹${Number(info.cheapest_price).toFixed(2)}`;
            if (platformEl) platformEl.textContent = `via ${info.cheapest_platform}`;
            if (pillEl) pillEl.textContent = (info.cheapest_platform || '?').slice(0, 1);
        });
    } catch (error) {
        // Swallow errors to avoid breaking the UI
    }
}

function renderCompareList(prices) {
    if (!compareList) return;
    if (!prices || !prices.length) {
        compareList.innerHTML = '<div class="compare-empty">No prices available</div>';
        return;
    }
    compareList.innerHTML = prices
        .map((item) => {
            const isCheapest = item.is_cheapest ? 'is-cheapest' : '';
            const badgeText = item.is_cheapest ? 'Best deal' : '';
            const platformUrl = getPlatformUrl(item.platform);
            const platformLabel = platformUrl
                ? `<a class="compare-link" href="${platformUrl}" target="_blank" rel="noopener noreferrer">${item.platform}</a>`
                : item.platform;
            return `
                <div class="compare-row ${isCheapest}">
                    <div class="compare-platform">
                        <span class="compare-initial">${(item.platform || '?')[0]}</span>
                        <div>
                            <div class="compare-name">${platformLabel}</div>
                            <div class="compare-sub">${badgeText}</div>
                        </div>
                    </div>
                    <div class="compare-price">\u20B9${Number(item.price).toFixed(2)}</div>
                </div>
            `;
        })
        .join('');
}

async function openCompareModal(button) {
    if (!compareModal || !compareList) return;
    compareTitle.textContent = button.dataset.productName || 'Product';
    compareMeta.textContent = button.dataset.productMeta || '';
    const imageSrc = button.dataset.productImage || '';
    if (compareImage) {
        compareImage.src = imageSrc;
        compareImage.alt = button.dataset.productName || 'Product image';
    }

    compareList.innerHTML = '<div class="compare-empty">Loading latest prices...</div>';

    const productId = button.dataset.productId;
    const productCategory = button.dataset.productCategory;
    if (productId) {
        try {
            const response = await fetch(`/api/product/${productCategory}/${productId}/prices`, { cache: 'no-store' });
            if (response.ok) {
                const payload = await response.json();
                renderCompareList(payload.prices || []);
            } else {
                const fallbackPrices = JSON.parse(button.dataset.prices || '[]');
                renderCompareList(fallbackPrices);
            }
        } catch (error) {
            const fallbackPrices = JSON.parse(button.dataset.prices || '[]');
            renderCompareList(fallbackPrices);
        }
    } else {
        const fallbackPrices = JSON.parse(button.dataset.prices || '[]');
        renderCompareList(fallbackPrices);
    }

    compareModal.classList.add('active');
    document.body.classList.add('modal-open');
}

function closeCompareModal() {
    if (!compareModal) return;
    compareModal.classList.remove('active');
    document.body.classList.remove('modal-open');
}

if (compareModal) {
    document.addEventListener('click', (event) => {
        const compareButton = event.target.closest('.compare-btn');
        if (compareButton) {
            openCompareModal(compareButton);
            return;
        }
        if (event.target.matches('[data-compare-close]') || event.target.closest('[data-compare-close]')) {
            closeCompareModal();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && compareModal.classList.contains('active')) {
            closeCompareModal();
        }
    });
}


refreshCardPrices();
setInterval(refreshCardPrices, CARD_REFRESH_INTERVAL_MS);


