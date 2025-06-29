#!/bin/bash

echo "إضافة main.py إلى git..."
git add main.py
echo "توثيق التعديلات..."
git commit -m "Add self-ping keep_alive thread to prevent Render spin down"
echo "رفع التعديلات إلى GitHub..."
git push origin main
echo "تم رفع التعديلات إلى GitHub بنجاح" 