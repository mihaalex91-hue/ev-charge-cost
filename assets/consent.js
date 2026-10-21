/* EV Charge Cost – Google Analytics with cookie consent (UK GDPR / PECR).
   Analytics cookies are OFF until the visitor clicks Accept. */
(function () {
  var GA = "G-Y9MR1QCPRG";
  var KEY = "evccConsent";
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  gtag("consent", "default", {
    analytics_storage: saved === "yes" ? "granted" : "denied",
    ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied"
  });
  gtag("js", new Date());
  gtag("config", GA);
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA;
  document.head.appendChild(s);

  function set(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
    gtag("consent", "update", { analytics_storage: v === "yes" ? "granted" : "denied" });
    var b = document.getElementById("evccCk");
    if (b) b.style.display = "none";
  }

  function bar() {
    var b = document.getElementById("evccCk");
    if (b) { b.style.display = "flex"; return; }
    b = document.createElement("div");
    b.id = "evccCk";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", "Cookie consent");
    b.style.cssText = "position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:580px;margin:0 auto;display:flex;flex-wrap:wrap;gap:10px;align-items:center;background:var(--surface,#fff);color:var(--ink,#16211C);border:1px solid var(--line,#D9DED9);border-radius:12px;padding:12px 14px;font-size:14px;line-height:1.4;box-shadow:0 6px 24px rgba(0,0,0,.18)";
    b.innerHTML = '<span style="flex:1;min-width:210px">Can we use Google Analytics cookies to see which pages help EV drivers most? No ads tracking. Your calculator inputs stay on your device.</span>' +
      '<button type="button" id="evccYes" class="btn" style="padding:8px 14px">Accept</button>' +
      '<button type="button" id="evccNo" class="btn quiet" style="padding:8px 14px">Decline</button>';
    document.body.appendChild(b);
    document.getElementById("evccYes").onclick = function () { set("yes"); };
    document.getElementById("evccNo").onclick = function () { set("no"); };
  }

  function init() {
    if (!saved) bar();
    var f = document.querySelector("footer");
    if (f) {
      var p = document.createElement("p");
      p.style.fontSize = ".85em";
      p.innerHTML = 'Privacy: we use Google Analytics cookies only if you accept them. <a href="#" id="evccSettings">Cookie settings</a>';
      f.appendChild(p);
      document.getElementById("evccSettings").onclick = function (e) { e.preventDefault(); bar(); };
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
