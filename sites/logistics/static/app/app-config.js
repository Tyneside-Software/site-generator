/**
 * Tyneside Logistics — app shell config
 * Backend: tyneside-api brand package app/brands/logistics
 *   https://github.com/Tyneside-Software/tyneside-api
 *
 * Set apiBaseUrl to the Cloud Run service (no trailing slash).
 */
window.TYNESIDE_LOGISTICS = {
  /**
   * Shared API — same host as charity/cleaning.
   * Leave empty for offline shell mode.
   */
  apiBaseUrl: "https://tyneside-api-git-975511976696.europe-west1.run.app",

  /** Only if Cloud Run has API_KEY set — sent as X-Tyneside-Key. */
  apiKey: "",

  brandId: "logistics",
  appName: "Tyneside Logistics",
};
