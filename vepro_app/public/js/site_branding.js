(function () {
	"use strict";

	var STYLE_ID = "site-branding-dynamic-css";
	var BADGE_ID = "site-branding-badge";

	window.site_branding = window.site_branding || {};

	// --- Matching -----------------------------------------------------------

	function matchesRule(rule) {
		var hostname = window.location.hostname;
		var href = window.location.href;
		var value = rule.match_value;

		try {
			var result;
			switch (rule.match_type) {
				case "Host Equals":
					result = hostname === value;
					break;
				case "Host Contains":
					result = hostname.indexOf(value) !== -1;
					break;
				case "URL Contains":
					result = href.indexOf(value) !== -1;
					break;
				case "Regex":
					result = new RegExp(value).test(href);
					break;
				default:
					result = false;
			}
			console.debug(
				"[site_branding] rule '" + rule.rule_name + "' (" + rule.match_type + " / '" + value + "') →",
				result ? "MATCH" : "no match",
				"| hostname:", hostname, "| href:", href
			);
			return result;
		} catch (_e) {
			console.warn("[site_branding] Error evaluating rule '" + rule.rule_name + "':", _e);
			return false;
		}
	}

	function findMatchingRule(rules) {
		// rules are already sorted by priority ASC from the server
		for (var i = 0; i < rules.length; i++) {
			if (matchesRule(rules[i])) {
				return rules[i];
			}
		}
		return null;
	}

	// --- CSS injection ------------------------------------------------------

	function applyCSS(css) {
		var el = document.getElementById(STYLE_ID);
		if (!el) {
			el = document.createElement("style");
			el.id = STYLE_ID;
			document.head.appendChild(el);
		}
		el.textContent = css;
	}

	// --- Badge --------------------------------------------------------------

	function badgePositionCSS(position) {
		switch (position) {
			case "Top Left":
				return "top:0;left:0;border-radius:0 0 6px 0;";
			case "Bottom Right":
				return "bottom:0;right:0;border-radius:6px 0 0 0;";
			case "Bottom Left":
				return "bottom:0;left:0;border-radius:0 6px 0 0;";
			default: // Top Right
				return "top:0;right:0;border-radius:0 0 0 6px;";
		}
	}

	function applyBadge(rule) {
		if (!rule.badge_enabled || !(rule.badge_text || "").trim()) {
			return;
		}

		var el = document.getElementById(BADGE_ID);
		if (!el) {
			el = document.createElement("div");
			el.id = BADGE_ID;
			document.body.appendChild(el);
		}

		var posCSS = badgePositionCSS(rule.badge_position || "Top Right");
		var bg = rule.badge_color || "#ff9800";
		var fg = rule.badge_text_color || "#ffffff";

		el.textContent = rule.badge_text;
		el.setAttribute(
			"style",
			"position:fixed;" +
				posCSS +
				"background:" +
				bg +
				";" +
				"color:" +
				fg +
				";" +
				"padding:6px 12px;" +
				"font-weight:700;" +
				"font-size:12px;" +
				"z-index:99999;" +
				"pointer-events:none;" +
				"font-family:sans-serif;" +
				"letter-spacing:0.5px;" +
				"line-height:1.4;"
		);
	}

	// --- Main ---------------------------------------------------------------

	function applyRule(rule) {
		console.log("[site_branding] Applying rule:", rule.rule_name, rule);
		if ((rule.css || "").trim()) {
			console.debug("[site_branding] Injecting CSS:", rule.css);
			applyCSS(rule.css);
		}
		applyBadge(rule);
		window.site_branding.active_rule = rule;
	}

	function init() {
		console.log("[site_branding] init – hostname:", window.location.hostname, "| href:", window.location.href);
		frappe.call({
			method: "vepro_app.site_branding.api.get_branding_rules",
			freeze: false,
			callback: function (response) {
				try {
					var rules = (response && response.message) || [];
					console.log("[site_branding] API returned", rules.length, "rule(s):", rules);
					var matched = findMatchingRule(rules);
					if (matched) {
						applyRule(matched);
					} else {
						console.log("[site_branding] No rule matched – nothing applied.");
					}
				} catch (_e) {
					console.error("[site_branding] Error in callback:", _e);
				}
			},
			error: function (err) {
				console.error("[site_branding] API call failed:", err);
			},
		});
	}

	$(document).ready(function () {
		init();
	});
})();
