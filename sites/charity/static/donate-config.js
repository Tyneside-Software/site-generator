/**
 * Charity donate config (GitHub Pages — no server for the static site).
 *
 * Backend: tyneside-api on Google Cloud Run
 *   https://github.com/Tyneside-Software/tyneside-api
 * Set apiBaseUrl after first Cloud Run deploy (no trailing slash).
 *
 * Tide Instant Checkout: create one reusable Instant Checkout item per amount
 * in the Tide app (Tyneside Cleaning account), then paste the URLs below.
 *
 * Tide cannot take a custom payment reference via URL. We match amount + date
 * in Tide and use the donate-intent API / donor line for the public list.
 */
window.TYNESIDE_DONATE = {
  gbpPerClean: 30,
  whatsappNumber: "447411949215",

  /**
   * Cloud Run service URL (or custom domain e.g. https://api.tyneside.group).
   * Leave empty until the API is deployed — form still works (Tide / donor WhatsApp).
   */
  apiBaseUrl: "https://tyneside-api-git-975511976696.europe-west1.run.app",

  /**
   * Only if Cloud Run has API_KEY set — sent as X-Tyneside-Key.
   * Visible in the browser; optional light gate only.
   */
  apiKey: "",

  /**
   * Tide Instant Checkout URLs (Tyneside Cleaning LTD products).
   * Mapped to the form amounts: £30 = 1 clean, £300 = 10, £3,000 = 100.
   * “10% clean” product used for the £3 “give a little” option.
   */
  tideLinks: {
    3: "https://pay.tide.co/products/10-clean-9f2kmNOX",
    30: "https://pay.tide.co/products/1-clean-cjhW2ivk",
    300: "https://pay.tide.co/products/10-cleans-uToHRCCV",
    3000: "https://pay.tide.co/products/100-cleans-fzWXRqLS",
  },

  itemTitles: {
    3: "Welcome-home clean donation · £3 (10% clean product)",
    30: "Welcome-home clean donation · £30 (1 clean)",
    300: "Welcome-home clean donation · £300 (10 cleans)",
    3000: "Welcome-home clean donation · £3,000 (100 cleans)",
  },
};
