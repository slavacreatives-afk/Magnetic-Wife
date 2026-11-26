(function () {
  var C = window.TMW || {};
  var STARTED_KEY = "tmw:checkout-started";
  var initiated = false;

  function track(name, params) {
    if (typeof window.fbq === "function") window.fbq("track", name, params || {});
    if (window.posthog && window.posthog.capture) window.posthog.capture(name, params || {});
  }
  function productParams() {
    return { content_name: "The Magnetic Wife", content_ids: "the-magnetic-wife", content_type: "product", value: C.value || 55, currency: "USD", num_items: 1 };
  }
  function initiate() {
    if (initiated) return;
    initiated = true;
    try { localStorage.setItem(STARTED_KEY, String(Date.now())); } catch (e) {}
    track("InitiateCheckout", productParams());
  }
  function withUtm(url) {
    try {
      var page = new URLSearchParams(location.search);
      var u = new URL(url);
      ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid"].forEach(function (k) {
        var v = page.get(k); if (v) u.searchParams.set(k, v);
      });
      return u.toString();
    } catch (e) { return url; }
  }

  // Offer label and end-date line
  document.querySelectorAll('[data-tmw="offerLabel"]').forEach(function (el) {
    if (C.offerLabel) el.textContent = C.offerLabel; else el.style.display = "none";
  });
  document.querySelectorAll('[data-tmw="offerUntil"]').forEach(function (el) {
    if (C.offerUntil) el.textContent = C.offerUntil; else el.style.display = "none";
  });

  // Checkout
  var wrap = document.getElementById("checkout");
  if (wrap && C.planId) {
    wrap.innerHTML = "";
    wrap.className += " embedded";
    var box = document.createElement("div");
    box.setAttribute("data-whop-checkout-plan-id", C.planId);
    box.setAttribute("data-whop-checkout-theme", "light");
    box.setAttribute("data-whop-checkout-hide-price", "true");
    if (C.returnUrl) box.setAttribute("data-whop-checkout-return-url", C.returnUrl);
    wrap.appendChild(box);
    var s = document.createElement("script");
    s.src = "https://js.whop.com/static/checkout/loader.js";
    s.async = true; s.defer = true;
    document.head.appendChild(s);
    // The checkout runs in an iframe: when she taps into it, the page loses focus.
    window.addEventListener("blur", function () {
      setTimeout(function () {
        var a = document.activeElement;
        if (a && a.tagName === "IFRAME" && wrap.contains(a)) initiate();
      }, 0);
    });
  } else if (wrap && C.checkoutUrl) {
    var btn = wrap.querySelector("a[data-buy]");
    if (btn) {
      btn.href = withUtm(C.checkoutUrl);
      btn.addEventListener("click", initiate);
    }
  } else if (wrap) {
    console.warn("The Magnetic Wife: add planId or checkoutUrl in config.js to switch on checkout.");
  }

  // ViewContent once she has started reading the story
  var story = document.getElementById("story-start");
  if (story && "IntersectionObserver" in window) {
    var seen = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!seen && en.boundingClientRect.top < 0 && !en.isIntersecting) {
          seen = true; track("ViewContent", productParams()); io.disconnect();
        }
      });
    });
    io.observe(story);
  }
})();
