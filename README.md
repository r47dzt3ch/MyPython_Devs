# AI QA Automation System

🤖 **Intelligent QA Testing with Gemini AI & Dynamic WebDriver**

An advanced automation system that combines AI-powered site analysis with dynamic web driver capabilities for comprehensive QA testing. The system uses Google's Gemini AI to intelligently analyze websites, detect login requirements, identify modules, and generate test scenarios automatically.

## 🌟 Features

### 🧠 AI-Powered Analysis
- **Intelligent Site Analysis**: Uses Gemini AI to analyze webpage content and structure
- **Login Detection**: Automatically detects if a site requires authentication
- **Module Identification**: Identifies and categorizes different sections/modules of a website
- **Test Scenario Generation**: Creates comprehensive test scenarios based on AI analysis

### 🌐 Dynamic WebDriver Support
- **Multi-Browser Support**: Chrome, Edge, Brave, Firefox with automatic fallback
- **Headless Mode**: Support for headless browser operation
- **Debug Port Connection**: Connect to existing browser instances
- **Cross-Platform**: Works on Windows, macOS, and Linux

### 📡 Firebase Real-time Control
- **Remote Operation**: Control the QA bot from a remote dashboard or application.
- **Real-time Commands**: Send test commands and receive results in real-time.
- **Bot Status Monitoring**: Monitor the bot's status (idle, running, error) via Firebase.

### 🔐 Smart Authentication
- **Login Detection**: AI identifies login requirements automatically
- **Credential Prompting**: Interactive credential collection for local mode.
- **Remote Credentials**: Securely pass credentials via Firebase commands.
- **Form Element Detection**: Intelligent identification of login form elements

### 🧪 Comprehensive Testing
- **Automated Test Generation**: AI creates relevant test scenarios
- **Interactive Module Selection**: User-friendly module selection interface
- **Batch Testing**: Test multiple URLs in sequence
- **Custom Test Scenarios**: Support for custom test implementations

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Chrome, Edge, Brave, or Firefox browser
- Internet connection for AI API calls

### API Requirements
- Google Gemini API key (free tier available)

## 🚀 Installation

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd ai-qa-automation

# Or download the files directly
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here

# Firebase Credentials (for remote control mode)
FIREBASE_SERVICE_ACCOUNT_KEY_PATH=path/to/your/serviceAccountKey.json
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com

# Optional Firebase Paths
FIREBASE_COMMAND_PATH=commands
FIREBASE_RESULTS_PATH=results
FIREBASE_BOT_STATUS_PATH=bot_status
```

**Getting a Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Sign in with your Google account.
3. Create a new API key.
4. Copy the key to your `.env` file.

**Getting Firebase Credentials:**
1. Go to your [Firebase Project Settings](https://console.firebase.google.com/) > **Service accounts**.
2. Click **Generate new private key** and save the downloaded JSON file.
3. Add the file path and your database URL to the `.env` file.

### 4. Verify Installation
```bash
python ai_qa_automation.py
```

## 📖 Usage

### Running in Firebase Mode (Remote Control)

To run the bot as a service that listens for commands from Firebase:

```bash
python ai_qa_automation.py --firebase
```

Or by running the dedicated example script:

```bash
python firebase_usage_example.py
```

The bot will start, connect to Firebase, and wait for new commands under the `commands` path in your Realtime Database.

#### Sending Commands via Firebase

To trigger a test, add a new entry to the `commands` node in your Firebase Realtime Database with a unique ID and a `status` of `pending`.

**Example Command:**
```json
{
  "commands": {
    "cmd_1678886400": {
      "action": "test_url",
      "payload": {
        "url": "https://your-test-site.com",
        "credentials": {
          "username": "your_username",
          "password": "your_password"
        }
      },
      "status": "pending"
    }
  }
}
```

The bot will pick up this command, update its status to `processing`, run the test, and push the results to the `results` node.

### Basic Interactive Usage (Local)

```python
from ai_qa_automation import AIQAAutomation

# Initialize the system
automation = AIQAAutomation(browser_preference='chrome', headless=False)

try:
    # Start session
    automation.start_session()
    
    # Run interactive session (prompts for URL and handles everything)
    automation.run_interactive_session()
    
finally:
    automation.close_session()
```

### Programmatic Usage

```python
from ai_qa_automation import AIQAAutomation

automation = AIQAAutomation()

try:
    automation.start_session()
    
    # Navigate to specific site
    analysis = automation.navigate_to_site("https://example.com")
    
    # Handle login if required
    if analysis.get('requires_login', False):
        automation.handle_login_if_required()
    
    # Generate and run tests
    automation.generate_and_display_test_scenarios()
    automation.run_automated_tests()
    
finally:
    automation.close_session()
```

### AI Analysis Only

```python
from ai_qa_automation import GeminiAI
from dynamic_webdriver import DynamicWebDriver

ai = GeminiAI()

# Analyze HTML content
analysis = ai.analyze_page_content(html_content, url)
print(f"Requires login: {analysis['requires_login']}")
print(f"Modules found: {analysis['main_modules']}")

# Generate test scenarios
scenarios = ai.generate_test_scenarios(analysis, url)
```

## 🎯 How It Works

### 1. Site Navigation & Analysis
```
User Input URL → Navigate with WebDriver → Extract HTML → AI Analysis
```

The system navigates to the provided URL and uses Gemini AI to analyze the page structure, identifying:
- Login requirements
- Available modules/sections
- Interactive elements
- Forms and navigation

### 2. Smart Login Handling
```
AI Detects Login → Prompt Credentials → Auto-fill Forms → Verify Success
```

When login is required, the system:
- Identifies login form elements using AI
- Prompts user for credentials
- Automatically fills and submits forms
- Verifies successful authentication

### 3. Module Selection & Testing
```
AI Identifies Modules → Generate Menu → User Selection → Create Test Scenarios
```

The system creates an intelligent menu of available modules and generates comprehensive test scenarios based on the selection.

### 4. Automated Testing
```
Execute Tests → Collect Results → Generate Reports → Save to File
```

Runs automated tests including:
- Page load verification
- Navigation testing
- Form validation
- Module accessibility

## 🔧 Configuration Options

### Browser Configuration
```python
# Browser preference (chrome, edge, brave, firefox)
automation = AIQAAutomation(browser_preference='chrome')

# Headless mode
automation = AIQAAutomation(headless=True)

# Connect to existing browser (debug mode)
automation = AIQAAutomation(debug_port=9222)
```

### AI Configuration
The system uses environment variables for AI configuration:
- `GEMINI_API_KEY`: Your Google Gemini API key

## 📊 Output & Results

### Console Output
The system provides real-time feedback:
- 🚀 Session initialization
- 🌐 Navigation status
- 🤖 AI analysis results
- 🔐 Login handling
- 🧪 Test execution
- 📊 Results summary

### Test Results
Results are automatically saved to JSON files:
```json
{
  "timestamp": "2024-01-15 10:30:00",
  "url": "https://example.com",
  "analysis": { ... },
  "tests_run": [ ... ],
  "summary": {
    "total": 5,
    "passed": 4,
    "failed": 1
  }
}
```

## 🎮 Interactive Features

### Module Selection Menu
```
🎯 AI-GENERATED MODULE SELECTION MENU
============================================================
1. Dashboard - Main application dashboard with key metrics
2. User Management - User administration and profile management
3. Reports - Data visualization and reporting tools
4. Settings - Application configuration and preferences

📋 AI Recommendations:
  • Start with Dashboard for overall functionality testing
  • Test User Management for CRUD operations
  • Verify Reports for data accuracy
============================================================
```

### Test Scenario Generation
The AI generates comprehensive test scenarios including:
- **Functional Tests**: Core functionality verification
- **UI Tests**: Interface and usability testing
- **Integration Tests**: Module interaction testing
- **Validation Tests**: Form and data validation

## 🛠️ Advanced Usage

### Custom Test Implementation
```python
def custom_test_function():
    """Implement your custom test logic"""
    try:
        # Your test code here
        return True  # Test passed
    except Exception as e:
        print(f"Test failed: {e}")
        return False  # Test failed

# Add to automation system
automation.custom_tests.append({
    "name": "Custom Test",
    "function": custom_test_function
})
```

### Batch Testing
```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

for url in urls:
    analysis = automation.navigate_to_site(url)
    automation.run_automated_tests()
```

## 🔍 Troubleshooting

### Common Issues

**1. Browser Driver Issues**
```
Error: Failed to initialize any browser driver
```
**Solution**: Ensure you have at least one supported browser installed. The system will try Chrome → Brave → Edge → Firefox in order.

**2. API Key Issues**
```
Error: GEMINI_API_KEY not found in environment variables
```
**Solution**: Create a `.env` file with your Gemini API key.

**3. Login Detection Issues**
```
Warning: Could not locate login elements
```
**Solution**: The AI might not have detected the login form correctly. You can manually specify selectors or try a different approach.

### Debug Mode
Enable debug mode for detailed logging:
```python
automation = AIQAAutomation(debug_port=9222)  # Connect to existing browser
```

## 🤝 Contributing

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

### Custom AI Prompts
You can customize AI prompts by modifying the `GeminiAI` class methods:
- `analyze_page_content()`: Site analysis prompts
- `generate_test_scenarios()`: Test generation prompts
- `suggest_module_selection()`: Module selection prompts

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: For intelligent content analysis
- **Selenium WebDriver**: For browser automation
- **BeautifulSoup**: For HTML parsing
- **WebDriver Manager**: For automatic driver management

## 📞 Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information
4. Include error messages and system information

---

**Made with ❤️ for the QA community**

*Empowering testers with AI-driven automation*