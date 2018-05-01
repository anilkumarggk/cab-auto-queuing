#!/usr/bin/env bash
ps auxww | grep 'celery -A vuedj' | awk '{print $2}' | xargs kill -9
celery -A vuedj worker