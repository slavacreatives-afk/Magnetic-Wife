/* ============================================================
   THE MAGNETIC WIFE: SITE SETTINGS
   This is the only file you need to edit for checkout and offer
   changes. Save, then upload the whole folder to Netlify again.
   ============================================================ */
window.TMW = {
  /* Your Whop Plan ID for the $55 plan, e.g. "plan_AbC123xyz".
     Whop dashboard > Checkout Links > ... (three dots) > Details.
     When this is filled in, the Whop checkout appears on the page. */
  planId: "",

  /* Backup: a normal Whop checkout link. Used only if planId is empty. */
  checkoutUrl: "https://whop.com/checkout/plan_YVuQRgCviQJLl/",

  /* Where Whop sends her after paying. */
  returnUrl: "https://happyspousehappyhouse.love/thank-you/?payment=success",

  /* Price used for Meta Pixel events (USD). */
  value: 55,

  /* Small label above the price, and the line under it.
     Set offerUntil to "" to hide that line. */
  offerLabel: "Early Black Friday price",
  offerUntil: "",

  /* Meta Pixel */
  pixelId: "2606152179826950"
};
