# Polygon.io Setup Guide

## Why Switch to Polygon.io?

Polygon.io offers several advantages over yfinance:
- ✅ **More Reliable**: Official API with better uptime
- ✅ **Better Data Quality**: Cleaner, more accurate market data
- ✅ **Faster**: Optimized API endpoints  
- ✅ **Official Support**: Proper documentation and support
- ✅ **Free Tier Available**: 5 API calls per minute with 15-minute delayed data

## Getting Your Free API Key

### Step 1: Sign Up
1. Go to [polygon.io](https://polygon.io/)
2. Click **"Get your free API Key"** or **"Sign Up"**
3. Fill in your details and create an account
4. Verify your email address

### Step 2: Get Your API Key
1. Log in to your Polygon.io dashboard
2. Navigate to **Dashboard** → **API Keys**
3. Copy your API key (it will look like: `your_api_key_here`)

### Step 3: Configure Your Project

#### Option A: Using .env File (Recommended)

1. Copy the `.env.example` file to create a new `.env` file:
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. Open the `.env` file in a text editor

3. Replace `your_polygon_api_key_here` with your actual API key:
   ```
   POLYGON_API_KEY=abc123def456ghi789
   ```

4. Save the file

#### Option B: Using Environment Variables

**Windows PowerShell:**
```powershell
$env:POLYGON_API_KEY="your_actual_api_key_here"
```

**Linux/Mac:**
```bash
export POLYGON_API_KEY="your_actual_api_key_here"
```

**Windows Command Prompt:**
```cmd
set POLYGON_API_KEY=your_actual_api_key_here
```

## Installing Required Packages

After setting up your API key, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `polygon-api-client` - Official Polygon.io Python client
- `python-dotenv` - For loading environment variables
- All other required dependencies

## Testing Your Setup

Run the setup check script to verify everything is working:

```bash
python setup_check.py
```

You should see:
```
✅ All dependencies installed
✅ Polygon.io API key found
✅ Successfully connected to Polygon.io
```

## Polygon.io Free Tier Limits

The free tier includes:
- **5 API calls per minute**
- **15-minute delayed data** for stocks
- **Unlimited history** (up to 2 years for most stocks)

### Rate Limiting Tips

Since the free tier has a 5 calls/minute limit:
1. **Portfolio Analysis**: Analyzing all 30+ stocks will take ~6-7 minutes
2. **Single Stock**: Works instantly with no delays
3. **Caching**: The app caches data to minimize API calls

### Upgrading (Optional)

If you need real-time data or higher limits:
- **Starter Plan** ($29/month): 100 calls/minute, real-time data
- **Developer Plan** ($99/month): 500 calls/minute
- **Advanced Plan** ($199/month): 1000 calls/minute

Visit [polygon.io/pricing](https://polygon.io/pricing) for details.

## Troubleshooting

### Error: "Polygon.io API key not found"
- Make sure your `.env` file is in the project root directory
- Check that the `.env` file contains `POLYGON_API_KEY=your_key`
- Ensure there are no spaces around the `=` sign
- Restart the application after creating/modifying `.env`

### Error: "401 Unauthorized"
- Your API key is invalid or expired
- Log in to polygon.io and verify your API key
- Make sure you copied the entire key without extra spaces

### Error: "429 Too Many Requests"
- You've exceeded the free tier limit (5 calls/minute)
- Wait 1 minute before trying again
- Consider upgrading to a paid plan for higher limits

### Error: "No data found for ticker"
- The ticker might not be supported or have limited data on Polygon
- Try a different ticker (AAPL, TSLA, etc.)
- Some micro-cap stocks may have limited historical data

## Security Best Practices

1. **Never commit your .env file**: It's already in `.gitignore`
2. **Don't share your API key**: Keep it private
3. **Regenerate if exposed**: If you accidentally share your key, regenerate it in your Polygon dashboard
4. **Use separate keys**: Use different keys for development and production

## Support

- **Polygon.io Documentation**: [polygon.io/docs](https://polygon.io/docs)
- **API Status**: [status.polygon.io](https://status.polygon.io)
- **Support**: support@polygon.io

## Migration from yfinance

All previous functionality remains the same. The app automatically uses Polygon.io instead of yfinance with these changes:

✅ Same function signatures (`fetch_hourly_data`, etc.)  
✅ Same return format (pandas DataFrame)  
✅ Better data quality and reliability  
✅ No breaking changes to your workflow  

The only difference is you need to configure your API key as described above.
