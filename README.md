# InboxPilot - CV Extractor & Email Generator

A comprehensive, production-ready system for extracting CV data, parsing job descriptions, and generating personalized emails using AI agents built with PydanticAI and Groq LLM.

## 📁 Project Structure

```
my_own/
├── 📄 Core Application Files
│   ├── main.py                    # Main Streamlit application entry point
│   ├── config.py                  # Configuration and model settings
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # This documentation file
│
├── 🤖 AI Agent Modules
│   ├── cv_extractor.py            # CV/Resume extraction agent and UI
│   ├── job_parser.py              # Job description parser with web scraping
│   ├── email_generator.py         # Email generator agent
│   └── email_tracker.py           # Email tracking and analytics
│
├── 🗄️ Data Storage & Management
│   ├── vector_store.py            # ChromaDB vector database operations
│   ├── chroma_db/                 # ChromaDB database files
│   │   ├── chroma.sqlite3         # Main database file
│   │   └── [collection_ids]/      # Vector collections
│   └── email_records.json         # Email tracking records
│
├── 🛠️ Utility & Support Files
│   ├── error_handler.py           # Centralized error handling
│   ├── debug_scraper.py           # Debug script for web scraping
│   ├── check_email_config.py      # Email configuration validator
│   └── run_tests.py               # Test runner for all components
│
├── 🧪 Test Scripts
│   ├── test_scripts/
│   │   ├── test_cv_extractor.py   # CV extraction tests
│   │   ├── test_scraper.py        # Web scraping tests
│   │   ├── test_link_extraction.py # Link extraction tests
│   │   ├── test_setup.py          # Environment setup tests
│   │   └── test_email_functionality.py # Email functionality tests
│
├── ⚙️ Setup & Configuration
│   ├── setup_scripts/
│   │   └── setup_env.py           # Environment setup automation
│   └── TROUBLESHOOTING.md         # Detailed troubleshooting guide
│
└── 📊 Generated Files
    ├── __pycache__/               # Python cache files
    └── email_records.json         # Email tracking data
```

## 🚀 Features

### 📄 CV/Resume Data Extraction

- **AI-Powered Parsing**: Extract structured data from PDF resumes using Groq LLM
- **Comprehensive Data**: Personal info, education, experience, volunteer work, skills, projects, awards, publications
- **Manual Link Management**: Add social media profiles and GitHub repositories with username-based input
- **Data Validation**: Detect placeholder/fake data and ensure quality
- **Chronological Sorting**: All time-based data sorted from latest to oldest

### 🔍 Job Description Parser

- **Dual Input Methods**: Manual text input or automatic web scraping from job URLs
- **Web Scraping**: Extract job information from major job sites using BeautifulSoup
- **Structured Extraction**: Parse job descriptions into organized data using AI
- **Comprehensive Job Data**: Title, company, location, skills, responsibilities, qualifications, benefits
- **Duplicate Prevention**: Check if emails were already sent to prevent spam
- **Email Tracking**: Monitor sent emails with statistics and success rates

### 📧 Email Generator

- **Personalized Content**: Generate emails using CV and job data for perfect matching
- **Multiple Email Types**: Industry positions, academic research, freelance, networking
- **Tone Customization**: Professional, friendly, confident, enthusiastic
- **Smart Personalization**: Match skills, experience, and projects to job requirements
- **Email Tracking**: Record sent emails with detailed metadata

### 📊 Email Tracking System

- **Duplicate Prevention**: Prevent sending multiple emails to same company/job
- **Statistics Dashboard**: Track total emails, companies contacted, success rates
- **Email History**: View recent emails with status and metadata
- **Data Persistence**: Store email records in JSON format

## 🏗️ Architecture

### Technology Stack

- **AI Framework**: PydanticAI for structured agents
- **LLM**: Groq (Llama 3.3 70B Versatile)
- **UI Framework**: Streamlit
- **Data Models**: Pydantic for type safety
- **PDF Processing**: PyPDF2
- **Web Scraping**: BeautifulSoup4, Requests
- **Vector Database**: ChromaDB for semantic search
- **Data Storage**: JSON files for persistence

### Core Components

#### 1. **Main Application (`main.py`)**

- Streamlit app entry point
- Navigation and session management
- Data flow coordination between modules

#### 2. **CV Extractor (`cv_extractor.py`)**

- PDF resume parsing with AI
- Structured data extraction
- Manual link management
- Data validation and quality checks

#### 3. **Job Parser (`job_parser.py`)**

- Web scraping from job sites
- Manual job description input
- AI-powered job data extraction
- URL validation and error handling

#### 4. **Email Generator (`email_generator.py`)**

- Personalized email generation
- Multiple email types and tones
- SMTP email sending integration
- Email preview and management

#### 5. **Vector Store (`vector_store.py`)**

- ChromaDB integration for semantic search
- CV and job data storage
- Data retrieval and management
- Collection management

#### 6. **Email Tracker (`email_tracker.py`)**

- Email history tracking
- Duplicate prevention
- Statistics and analytics
- Data persistence

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd my_own
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   ```bash
   # Option 1: Create .env file (recommended for local development)
   cp env_example.txt .env
   # Edit .env with your Groq API key and email settings

   # Option 2: Use Streamlit secrets (see SECRETS_MANAGEMENT.md for details)
   ```

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## 📋 Usage Workflow

### Step 1: CV Extractor

1. **Upload CV/Resume**: Upload your PDF resume
2. **Extract Data**: AI extracts structured information
3. **Add Social Links**: Enter usernames for social platforms
4. **Review & Download**: Verify extracted data and download

### Step 2: Job Parser

1. **Choose Input Method**:
   - **Manual Text Input**: Paste job description text
   - **Job URL Scraping**: Enter job posting URL for automatic extraction
2. **Parse Job Data**: AI extracts structured job information
3. **Check Duplicates**: System warns if email already sent
4. **Review Details**: Verify extracted job requirements

### Step 3: Email Generator

1. **Configure Settings**: Choose email type and tone
2. **Add Recipient Info**: Enter hiring manager details (optional)
3. **Generate Email**: AI creates personalized email
4. **Review & Send**: Preview, download, or mark as sent

## 🌐 Supported Job Sites

The web scraper supports the following job posting sites:

- **LinkedIn Jobs**: `linkedin.com/jobs`
- **Indeed**: `indeed.com`
- **Glassdoor**: `glassdoor.com`
- **Monster**: `monster.com`
- **CareerBuilder**: `careerbuilder.com`
- **ZipRecruiter**: `ziprecruiter.com`
- **Dice**: `dice.com`
- **Angel.co**: `angel.co`
- **Stack Overflow Jobs**: `stackoverflow.com/jobs`
- **GitHub Jobs**: `github.com/jobs`
- **Remote.co**: `remote.co`
- **WeWorkRemotely**: `weworkremotely.com`
- **FlexJobs**: `flexjobs.com`

### Web Scraping Features

- **Automatic Detection**: Validates URLs against supported job sites
- **Smart Extraction**: Uses multiple selectors to find job information
- **Fallback Methods**: Extracts from page title and URL if specific elements not found
- **Error Handling**: Graceful handling of network issues and parsing errors
- **User-Agent Spoofing**: Uses realistic browser headers to avoid blocking

## 📊 Data Models

### CV Data Structure

```json
{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "Phone Number",
  "education": ["Degree, Institution, Year, GPA"],
  "experience": ["Job Title, Company, Year"],
  "volunteer": ["Volunteer Role, Organization, Year"],
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "projects": ["Project Name, Year"],
  "awards": ["Award Name, Year"],
  "publications": ["Publication Title, Year"],
  "summary": "Professional summary",
  "manual_links": {
    "LinkedIn": "https://linkedin.com/in/username",
    "GitHub": "https://github.com/username",
    "Portfolio": "https://portfolio.com"
  }
}
```

### Job Data Structure

```json
{
  "job_title": "Software Engineer",
  "company_name": "Tech Corp",
  "location": "San Francisco, CA",
  "job_type": "Full-time",
  "experience_level": "Senior",
  "required_skills": ["Python", "React", "AWS"],
  "preferred_skills": ["Docker", "Kubernetes"],
  "responsibilities": ["Develop features", "Code review"],
  "qualifications": ["Bachelor's degree", "5+ years experience"],
  "benefits": ["Health insurance", "401k"],
  "salary_range": "$120k-$150k",
  "industry": "Technology",
  "department": "Engineering",
  "remote_policy": "Hybrid",
  "visa_sponsorship": true,
  "summary": "Brief job summary"
}
```

### Email Record Structure

```json
{
  "id": "unique-identifier",
  "job_title": "Software Engineer",
  "company_name": "Tech Corp",
  "recipient_email": "hiring@techcorp.com",
  "recipient_name": "John Smith",
  "sent_date": "2024-01-15T10:30:00",
  "email_type": "Industry Position",
  "status": "sent",
  "cv_data_used": {...},
  "job_data_used": {...},
  "email_content": "Full email content",
  "notes": "Additional notes"
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required: Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Optional: Email Configuration
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_PASSWORD=your_app_password
SENDER_NAME=Your Name

# Optional: Model Configuration
GROQ_MODEL=llama-3.3-70b-versatile
```

### Model Configuration

The system uses Groq's Llama 3.3 70B model for accurate data extraction and email generation. You can modify the model in `config.py`:

```python
GROQ_MODEL = "llama-3.3-70b-versatile"
```

## 🧪 Testing

### Test Runner

Use the comprehensive test runner for all components:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py cv          # CV extraction tests
python run_tests.py scraper     # Web scraping tests
python run_tests.py email       # Email functionality tests
python run_tests.py setup       # Environment setup tests
python run_tests.py email_config # Email configuration tests
```

### Individual Test Scripts

```bash
# CV extraction tests
python test_scripts/test_cv_extractor.py

# Web scraping tests
python test_scripts/test_scraper.py

# Link extraction tests
python test_scripts/test_link_extraction.py

# Setup tests
python test_scripts/test_setup.py

# Email functionality tests
python test_scripts/test_email_functionality.py
```

### Debug Tools

```bash
# Debug web scraping
python debug_scraper.py

# Check email configuration
python check_email_config.py
```

## 🔧 Key Features

### Smart Personalization

- **Skill Matching**: Automatically match CV skills to job requirements
- **Experience Alignment**: Connect relevant experience to job responsibilities
- **Project Highlighting**: Reference specific projects that align with job needs
- **Social Integration**: Include relevant social links and portfolio

### Web Scraping Capabilities

- **Multi-Site Support**: Works with major job posting platforms
- **Intelligent Parsing**: Uses multiple strategies to extract job information
- **Robust Error Handling**: Graceful degradation when scraping fails
- **Rate Limiting**: Respectful scraping with delays and user-agent headers

### Email Tracking & Analytics

- **Duplicate Prevention**: 30-day cooldown for same company/job combinations
- **Success Metrics**: Track delivery, open, and reply rates
- **Company Analytics**: Monitor engagement across different companies
- **Email History**: Complete audit trail of all sent emails

### Production-Ready Features

- **Error Handling**: Comprehensive error handling and user feedback
- **Data Validation**: Input validation and quality checks
- **Session Management**: Persistent data across application sessions
- **Modular Architecture**: Easy to extend and maintain

## 🎯 Use Cases

### Job Seekers

- **Mass Applications**: Efficiently apply to multiple positions
- **Personalized Outreach**: Stand out with tailored emails
- **Application Tracking**: Monitor all applications in one place
- **Performance Analytics**: Track which approaches work best

### Recruiters

- **Candidate Assessment**: Quickly parse and evaluate CVs
- **Job Description Analysis**: Extract key requirements and benefits
- **Communication Tracking**: Monitor outreach effectiveness

### Career Coaches

- **Client Support**: Help clients create personalized applications
- **Strategy Development**: Analyze successful application patterns
- **Performance Tracking**: Monitor client application success rates

## 🚀 Advanced Features

### Email Templates

- **Industry-Specific**: Templates for different job types
- **Tone Variations**: Professional, friendly, confident, enthusiastic
- **Customization**: Easy to modify and extend templates

### Analytics Dashboard

- **Success Metrics**: Track email performance
- **Company Insights**: Analyze which companies respond best
- **Timing Analysis**: Optimize send times for better response rates

### Integration Ready

- **API Endpoints**: RESTful API for external integrations
- **Webhook Support**: Real-time notifications for email events
- **Export Options**: Multiple format support for data export

## 📧 Email Sending Functionality

The application includes direct email sending capabilities through SMTP. You can send generated emails directly from the application.

### Email Setup

1. **Enable 2-Factor Authentication** on your email account
2. **Generate an App Password**:
   - **Gmail**: Google Account → Security → App Passwords
   - **Outlook**: Account Settings → Security → App Passwords
   - **Yahoo**: Account Security → App Passwords
3. **Configure Environment Variables**: Add your email credentials to the `.env` file:
   ```
   EMAIL_ADDRESS=your.email@gmail.com
   EMAIL_PASSWORD=your_app_password
   SENDER_NAME=Your Name
   ```
4. **Restart Application**: The app will automatically use your configured email settings

### Supported Email Providers

- **Gmail**: `smtp.gmail.com:587`
- **Outlook/Office365**: `smtp.outlook.com:587`
- **Yahoo**: `smtp.yahoo.com:587`

### Testing Email Functionality

```bash
# Test email configuration
python run_tests.py email_config

# Test email functionality
python run_tests.py email
```

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**

   - Ensure `GROQ_API_KEY` is set in `.env` file
   - Verify the API key is valid and has sufficient credits
   - Check network connectivity

2. **Email Configuration Problems**

   - Run `python check_email_config.py` to diagnose issues
   - Ensure 2FA is enabled and app password is generated
   - Verify SMTP settings for your email provider

3. **Web Scraping Issues**

   - Some job sites may block automated requests
   - Try different job URLs or use manual input
   - Check the debug output for specific error messages

4. **Data Persistence Issues**
   - Ensure write permissions in the project directory
   - Check if ChromaDB files are corrupted
   - Verify JSON file permissions

### Debug Steps

1. **Enable Debug Mode**: Check "Show Debug Options" in the app
2. **Run Test Suite**: Use `python run_tests.py` to identify issues
3. **Check Logs**: Review error messages and debug output
4. **Verify Configuration**: Ensure all environment variables are set correctly

For detailed troubleshooting, see `TROUBLESHOOTING.md`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- [x] Email sending integration (SMTP, Gmail API) ✅
- [x] Web scraping for job descriptions ✅
- [x] Vector database integration ✅
- [x] Email tracking and analytics ✅
- [ ] AI-powered follow-up email generation
- [ ] User session management
- [ ] Email tracking management
