#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <cctype>
#include <iomanip>

const std::set<std::string> COMMON_PASSWORDS = {
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "monkey", "1234567890", "superman",
    "iloveyou", "sunshine", "princess", "dragon", "master",
    "welcome", "login", "admin123", "pass", "test123",
    "password1", "12345678", "shadow", "football", "baseball"
};

const std::string RED    = "\033[91m";
const std::string YELLOW = "\033[93m";
const std::string GREEN  = "\033[92m";
const std::string CYAN   = "\033[96m";
const std::string BOLD   = "\033[1m";
const std::string RESET  = "\033[0m";

struct CheckResult {
    std::string strength;     // WEAK / MEDIUM / STRONG
    int         score;
    bool        has_upper;
    bool        has_lower;
    bool        has_digit;
    bool        has_symbol;
    bool        is_common;
    bool        has_repeats;
    int         length;
    std::vector<std::string> feedback;
};

std::string to_lower(const std::string& s) {
    std::string result = s;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c){ return std::tolower(c); });
    return result;
}

bool is_common_password(const std::string& password) {
    std::string lower = to_lower(password);
    return COMMON_PASSWORDS.count(lower) > 0;
}

bool has_repeated_chars(const std::string& password) {
    for (size_t i = 0; i + 2 < password.size(); ++i) {
        if (password[i] == password[i+1] && password[i+1] == password[i+2]) {
            return true;
        }
    }
    return false;
}

void check_variety(const std::string& password,
                   bool& has_upper, bool& has_lower,
                   bool& has_digit, bool& has_symbol) {
    has_upper  = false;
    has_lower  = false;
    has_digit  = false;
    has_symbol = false;
    std::string symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?/`~\"\\";

    for (char c : password) {
        if (std::isupper((unsigned char)c)) has_upper  = true;
        else if (std::islower((unsigned char)c)) has_lower  = true;
        else if (std::isdigit((unsigned char)c)) has_digit  = true;
        else if (symbols.find(c) != std::string::npos) has_symbol = true;
    }
}

CheckResult calculate_strength(const std::string& password) {
    CheckResult result;
    result.length = static_cast<int>(password.size());
    result.score  = 0;

    if (password.empty()) {
        result.strength = "INVALID";
        result.feedback.push_back("Password cannot be empty.");
        return result;
    }

    if (result.length < 8) {
        result.feedback.push_back("Too short — minimum 8 characters required.");
    } else if (result.length >= 16) {
        result.score += 3;
    } else if (result.length >= 12) {
        result.score += 2;
    } else {
        result.score += 1;
    }
    result.is_common = is_common_password(password);
    if (result.is_common) {
        result.feedback.push_back("Commonly used password — easily cracked.");
        result.score = 0;
    }

    check_variety(password,
                  result.has_upper, result.has_lower,
                  result.has_digit, result.has_symbol);

    int variety_score = (result.has_upper ? 1 : 0)
                      + (result.has_lower ? 1 : 0)
                      + (result.has_digit ? 1 : 0)
                      + (result.has_symbol ? 1 : 0);
    result.score += variety_score;

    if (!result.has_upper)  result.feedback.push_back("Add an uppercase letter (A-Z).");
    if (!result.has_digit)  result.feedback.push_back("Add a number (0-9).");
    if (!result.has_symbol) result.feedback.push_back("Add a symbol (e.g. @, #, !).");
    if (!result.has_lower)  result.feedback.push_back("Add a lowercase letter.");

    result.has_repeats = has_repeated_chars(password);
    if (result.has_repeats) {
        result.score -= 1;
        result.feedback.push_back("Avoid repeating characters (e.g. 'aaa' or '111').");
    }

    result.score = std::max(0, result.score);

    if (result.is_common || result.length < 8) {
        result.strength = "WEAK";
    } else if (result.score <= 3) {
        result.strength = "WEAK";
    } else if (result.score <= 5) {
        result.strength = "MEDIUM";
    } else {
        result.strength = "STRONG";
    }

    if (result.feedback.empty()) {
        result.feedback.push_back("Password looks solid. Good work!");
    }

    return result;
}


void print_result(const CheckResult& r, const std::string& password) {
    std::string color;
    std::string banner;

    if (r.strength == "STRONG") {
        color  = GREEN;
        banner = "✅  STRONG PASSWORD — Good to go";
    } else if (r.strength == "MEDIUM") {
        color  = YELLOW;
        banner = "⚠️   MEDIUM PASSWORD — Can be improved";
    } else {
        color  = RED;
        banner = "❌  WEAK PASSWORD — Not acceptable";
    }

    std::string masked(password.size(), '*');

    std::cout << "\n" << std::string(47, '-') << "\n";
    std::cout << "  Password   : " << masked          << "\n";
    std::cout << "  Length     : " << r.length         << " characters\n";
    std::cout << "  Score      : " << r.score          << " / 7\n";
    std::cout << "\n  " << BOLD << color << banner << RESET << "\n";
    std::cout << std::string(47, '-') << "\n";

    std::cout << "\n  Character Mix:\n";
    std::cout << "    Uppercase : " << (r.has_upper  ? "✓" : "✗") << "\n";
    std::cout << "    Lowercase : " << (r.has_lower  ? "✓" : "✗") << "\n";
    std::cout << "    Numbers   : " << (r.has_digit  ? "✓" : "✗") << "\n";
    std::cout << "    Symbols   : " << (r.has_symbol ? "✓" : "✗") << "\n";

    if (!r.feedback.empty()) {
        std::cout << "\n  Suggestions:\n";
        for (const auto& tip : r.feedback) {
            std::cout << "    → " << tip << "\n";
        }
    }

    std::cout << "\n" << std::string(47, '-') << "\n\n";
}

int main() {
    std::cout << "\n" << BOLD << CYAN;
    std::cout << "=======================================================\n";
    std::cout << "   🔐  PASSWORD STRENGTH CHECKER  (C++ Version)\n";
    std::cout << "   DecodeLabs | Cybersecurity Project 1\n";
    std::cout << "=======================================================\n";
    std::cout << RESET;
    std::cout << "  Type a password to check its strength.\n";
    std::cout << "  Type 'quit' to exit.\n\n";

    std::string password;

    while (true) {
        std::cout << "  Enter password: ";

        // Note: in a real system use platform-specific echo-off.
        // For this training project, normal getline is fine.
        if (!std::getline(std::cin, password)) break;

        if (password == "quit" || password == "exit" || password == "q") {
            std::cout << "\n  " << CYAN << "Exiting. Stay secure! 🔒" << RESET << "\n\n";
            break;
        }

        CheckResult result = calculate_strength(password);
        print_result(result, password);
    }

    return 0;
}
