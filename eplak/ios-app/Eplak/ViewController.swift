import UIKit
import WebKit

class ViewController: UIViewController, WKNavigationDelegate, WKUIDelegate, WKScriptMessageHandler, UIGestureRecognizerDelegate {

    private var webView: WKWebView!
    private var activityIndicator: UIActivityIndicatorView!

    override var preferredStatusBarStyle: UIStatusBarStyle {
        return .lightContent
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupWebView()
        setupBackGesture()
        loadWebContent()
    }

    private func setupUI() {
        view.backgroundColor = UIColor(red: 13/255.0, green: 21/255.0, blue: 39/255.0, alpha: 1.0) // #0d1527
    }

    private func setupWebView() {
        let configuration = WKWebViewConfiguration()
        let contentController = WKUserContentController()

        // Register script message handler for bridge calls: window.webkit.messageHandlers.iOSApp.postMessage(...)
        contentController.add(self, name: "iOSApp")
        configuration.userContentController = contentController

        // Enable media playback and local file access
        configuration.allowsInlineMediaPlayback = true
        configuration.preferences.javaScriptCanOpenWindowsAutomatically = true
        configuration.defaultWebpagePreferences.allowsContentJavaScript = true

        webView = WKWebView(frame: .zero, configuration: configuration)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.backgroundColor = .clear
        webView.isOpaque = false
        webView.scrollView.backgroundColor = .clear
        webView.scrollView.bounces = false
        webView.scrollView.contentInsetAdjustmentBehavior = .never

        view.addSubview(webView)

        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: view.topAnchor),
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            webView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])

        // Loading indicator
        activityIndicator = UIActivityIndicatorView(style: .large)
        activityIndicator.color = .white
        activityIndicator.translatesAutoresizingMaskIntoConstraints = false
        activityIndicator.hidesWhenStopped = true
        view.addSubview(activityIndicator)

        NSLayoutConstraint.activate([
            activityIndicator.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            activityIndicator.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])

        activityIndicator.startAnimating()
    }

    private func setupBackGesture() {
        // Edge pan gesture from right/left for back navigation matching RTL
        let edgePan = UIScreenEdgePanGestureRecognizer(target: self, action: #selector(handleEdgePan(_:)))
        edgePan.edges = .right // Right edge for Persian RTL layout
        edgePan.delegate = self
        view.addGestureRecognizer(edgePan)

        let leftEdgePan = UIScreenEdgePanGestureRecognizer(target: self, action: #selector(handleEdgePan(_:)))
        leftEdgePan.edges = .left
        leftEdgePan.delegate = self
        view.addGestureRecognizer(leftEdgePan)
    }

    @objc private func handleEdgePan(_ recognizer: UIScreenEdgePanGestureRecognizer) {
        if recognizer.state == .ended {
            triggerJavaScriptBack()
        }
    }

    private func triggerJavaScriptBack() {
        let js = """
        (function() {
            if (typeof window.handleAppBack === 'function') {
                return window.handleAppBack(false);
            } else if (typeof window.goBack === 'function') {
                return window.goBack();
            }
            return false;
        })();
        """
        webView.evaluateJavaScript(js) { [weak self] (result, error) in
            guard let self = self else { return }
            let handled = (result as? Bool) ?? false
            if !handled && self.webView.canGoBack {
                self.webView.goBack()
            }
        }
    }

    private func loadWebContent() {
        // Check for bundled Web directory
        if let webDirPath = Bundle.main.path(forResource: "Web", ofType: nil),
           let indexUrl = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "Web") {
            let webDirUrl = URL(fileURLWithPath: webDirPath)
            webView.loadFileURL(indexUrl, allowingReadAccessTo: webDirUrl)
            return
        }

        // Fallback: root bundled index.html
        if let indexUrl = Bundle.main.url(forResource: "index", withExtension: "html") {
            let baseDir = indexUrl.deletingLastPathComponent()
            webView.loadFileURL(indexUrl, allowingReadAccessTo: baseDir)
            return
        }

        // Development fallback: localhost or preview server
        if let fallbackUrl = URL(string: "http://localhost:8080") {
            webView.load(URLRequest(url: fallbackUrl))
        }
    }

    // MARK: - WKScriptMessageHandler
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        guard message.name == "iOSApp", let body = message.body as? [String: Any] else { return }

        let action = body["action"] as? String

        switch action {
        case "haptic":
            let style = body["style"] as? String ?? "medium"
            triggerHaptic(style: style)
        case "exitApp":
            // iOS apps shouldn't forcefully exit according to Apple HIG, but suspend if requested
            UIControl().sendAction(#selector(NSXPCConnection.suspend), to: UIApplication.shared, for: nil)
        case "share":
            if let text = body["text"] as? String {
                let activityVC = UIActivityViewController(activityItems: [text], applicationActivities: nil)
                present(activityVC, animated: true)
            }
        default:
            break
        }
    }

    private func triggerHaptic(style: String) {
        switch style {
        case "light":
            UIImpactFeedbackGenerator(style: .light).impactOccurred()
        case "heavy":
            UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
        case "success":
            UINotificationFeedbackGenerator().notificationOccurred(.success)
        case "warning":
            UINotificationFeedbackGenerator().notificationOccurred(.warning)
        case "error":
            UINotificationFeedbackGenerator().notificationOccurred(.error)
        default:
            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
        }
    }

    // MARK: - WKNavigationDelegate
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        activityIndicator.stopAnimating()
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        activityIndicator.stopAnimating()
    }

    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        guard let url = navigationAction.request.url else {
            decisionHandler(.cancel)
            return
        }

        // Handle external protocols (tel, mailto, sms, maps)
        let scheme = url.scheme?.lowercased() ?? ""
        if scheme == "tel" || scheme == "mailto" || scheme == "sms" {
            if UIApplication.shared.canOpenURL(url) {
                UIApplication.shared.open(url)
            }
            decisionHandler(.cancel)
            return
        }

        decisionHandler(.allow)
    }

    // MARK: - WKUIDelegate (Native Alerts)
    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alert = UIAlertController(title: "ای‌پلاک", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "متوجه شدم", style: .default) { _ in completionHandler() })
        present(alert, animated: true)
    }

    func webView(_ webView: WKWebView, runJavaScriptConfirmPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping (Bool) -> Void) {
        let alert = UIAlertController(title: "ای‌پلاک", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "تایید", style: .default) { _ in completionHandler(true) })
        alert.addAction(UIAlertAction(title: "انصراف", style: .cancel) { _ in completionHandler(false) })
        present(alert, animated: true)
    }
}
