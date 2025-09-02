
import SwiftUI

@main
struct FalowenApp: App {
    @StateObject private var auth = AuthViewModel()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(auth)
                .task {
                    await ServerResolver.shared.discover()
                    await auth.bootstrap()
                }
        }
    }
}
