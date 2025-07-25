This project was an assignment to learn how to build a web service with Python. It helped me understand how to create web endpoints, store data, and write tests to make sure everything works.

This is a simple web application that shortens long URLs (like `https://www.example.com/very/long/url`) into short ones (like `http://localhost:5000/abc123`). It’s built using Python and Flask, a tool that helps create web apps. The app also tracks how many times a short URL is clicked and handles errors, like when someone enters an invalid URL.

## What can this app do?
**Shorten URLs**: You send a long URL, and the app gives you a short code (e.g., `abc123`) and a short link (e.g., `http://localhost:5000/abc123`).
 
 **Redirect**: When you visit the short link, it takes you to the original long URL.
 
 **Track Clicks**: The app counts how many times a short link is clicked and shows details like the original URL and creation time.

 **Handle Errors**: If you send a bad URL or a wrong short code, the app shows a clear error message.
