import streamlit as st
import re
from typing import Optional, Dict, Any


def handle_groq_api_error(error: Exception, context: str = "operation") -> None:
    """
    Centralized error handling for Groq API errors
    
    Args:
        error: The exception that occurred
        context: Context of the operation (e.g., "CV extraction", "job parsing", "email generation")
    """
    error_message = str(error)
    
    # Handle specific Groq API errors
    if "429" in error_message and "rate_limit_exceeded" in error_message:
        _handle_rate_limit_error(error_message)
        
    elif "401" in error_message or "unauthorized" in error_message.lower():
        _handle_auth_error()
        
    elif "model" in error_message.lower() and "not found" in error_message.lower():
        _handle_model_error()
        
    elif "timeout" in error_message.lower():
        _handle_timeout_error()
        
    else:
        _handle_generic_error(error, context)


def _handle_rate_limit_error(error_message: str) -> None:
    """Handle rate limit exceeded errors"""
    # Extract time remaining from error message
    time_match = re.search(r'Please try again in (\d+h\d+m\d+\.\d+s)', error_message)
    time_remaining = time_match.group(1) if time_match else "some time"
    
    st.error("🚫 **Rate Limit Exceeded**")
    st.error(f"**Error:** You've reached your daily token limit for Groq API")
    st.error(f"**Time remaining:** {time_remaining}")
    st.error("**Solutions:**")
    st.error("• Wait for the rate limit to reset")
    st.error("• Upgrade to Dev Tier at https://console.groq.com/settings/billing")
    st.error("• Try again later")
    
    # Show current usage info if available
    if "Limit" in error_message and "Used" in error_message:
        limit_match = re.search(r'Limit (\d+)', error_message)
        used_match = re.search(r'Used (\d+)', error_message)
        if limit_match and used_match:
            limit = int(limit_match.group(1))
            used = int(used_match.group(1))
            percentage = (used / limit) * 100
            st.progress(percentage / 100)
            st.write(f"**Usage:** {used:,} / {limit:,} tokens ({percentage:.1f}%)")


def _handle_auth_error() -> None:
    """Handle authentication errors"""
    st.error("🔑 **Authentication Error**")
    st.error("**Error:** Invalid or missing Groq API key")
    st.error("**Solutions:**")
    st.error("• Check your GROQ_API_KEY in the .env file")
    st.error("• Get a new API key from https://console.groq.com/keys")
    st.error("• Restart the application after updating the key")


def _handle_model_error() -> None:
    """Handle model not found errors"""
    st.error("🤖 **Model Error**")
    st.error("**Error:** The specified model is not available")
    st.error("**Solutions:**")
    st.error("• Check the model name in config.py")
    st.error("• Try a different model from the available options")
    st.error("• Contact Groq support if the issue persists")


def _handle_timeout_error() -> None:
    """Handle timeout errors"""
    st.error("⏰ **Timeout Error**")
    st.error("**Error:** Request timed out")
    st.error("**Solutions:**")
    st.error("• Check your internet connection")
    st.error("• Try again in a few minutes")
    st.error("• The request might be too large")


def _handle_generic_error(error: Exception, context: str) -> None:
    """Handle generic errors"""
    error_message = str(error)
    
    st.error(f"❌ **{context.title()} Error**")
    st.error(f"**Error:** {error_message}")
    st.error("**Possible Solutions:**")
    st.error("• Check your internet connection")
    st.error("• Verify your Groq API key is valid")
    st.error("• Try again with different input")
    st.error("• Contact support if the issue persists")
    
    # Show debug info in expander
    with st.expander("🔍 Debug Information"):
        st.write(f"**Error Type:** {type(error).__name__}")
        st.write(f"**Full Error:** {error_message}")
        st.write("**Troubleshooting:**")
        st.write("1. Check your .env file has GROQ_API_KEY")
        st.write("2. Verify the API key at https://console.groq.com/keys")
        st.write("3. Check your Groq account status and billing")


def extract_rate_limit_info(error_message: str) -> Optional[Dict[str, Any]]:
    """
    Extract rate limit information from error message
    
    Returns:
        Dict with limit, used, percentage, and time_remaining, or None if not found
    """
    try:
        # Extract time remaining
        time_match = re.search(r'Please try again in (\d+h\d+m\d+\.\d+s)', error_message)
        time_remaining = time_match.group(1) if time_match else None
        
        # Extract usage info
        limit_match = re.search(r'Limit (\d+)', error_message)
        used_match = re.search(r'Used (\d+)', error_message)
        
        if limit_match and used_match:
            limit = int(limit_match.group(1))
            used = int(used_match.group(1))
            percentage = (used / limit) * 100
            
            return {
                "limit": limit,
                "used": used,
                "percentage": percentage,
                "time_remaining": time_remaining
            }
    except:
        pass
    
    return None 