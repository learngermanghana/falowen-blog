import Foundation

actor TokenStore {
    static let shared = TokenStore()

    private let accountKey = "falowen.tokenpair"
    private var refreshTask: Task<TokenPair, Error>?

    func currentPair() throws -> TokenPair {
        guard let pair: TokenPair = try Keychain.shared.readCodable(TokenPair.self, account: accountKey)
        else { throw URLError(.userAuthenticationRequired) }
        return pair
    }

    func save(_ pair: TokenPair) throws {
        try Keychain.shared.saveCodable(pair, account: accountKey)
    }

    /// Returns a valid pair; refreshes if expiring within 60s.
    func ensureFreshPair() async throws -> TokenPair {
        var pair = try currentPair()
        if pair.expiry <= Date().addingTimeInterval(60) {
            pair = try await refresh(using: pair.refreshToken)
        }
        return pair
    }

    /// Single-flight refresh: concurrent callers await the same task.
    func refresh(using refreshToken: String) async throws -> TokenPair {
        if let t = refreshTask { return try await t.value }
        let t = Task {
            let newPair = try await AuthAPI.refresh(using: refreshToken)
            try await self.saveAsync(newPair)
            return newPair
        }
        refreshTask = t
        defer { refreshTask = nil }
        return try await t.value
    }

    private func saveAsync(_ pair: TokenPair) async throws { try save(pair) }

    func clear() throws {
        try Keychain.shared.delete(account: accountKey)
    }
}
