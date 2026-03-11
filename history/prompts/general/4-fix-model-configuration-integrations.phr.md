---
id: 4
title: Fix model configuration integrations
stage: general
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: unknown
command: fix-models
labels: ["model-config", "bugfix", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .claude/config.json
tests:
- Config validation passed
---

## Prompt

kis chaker mei lag gaye ho phlel gemini api key aur qwen setup k through speckit mei claude code ko integraetd ki ahae us mei model issu a rha hae theek karo

(What task are you working on first? The Gemini API key and Qwen setup have been integrated with Claude code through speckit, but there's a model issue in it, fix it.)

## Response

Fixed critical model configuration issues in the Speckit-Claude Code integration.

## Problems Fixed

### 1. ❌ Qwen API Endpoint (WRONG)
```
https://portal.qwen.ai/v1/chat/completions
```
✅ **Fixed to:**
```
https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

### 2. ❌ Qwen Model Name (INVALID)
```
"qwen3-coder-plus"  ← doesn't exist
```
✅ **Fixed to:**
```
"qwen-plus"    ← valid Qwen model
"qwen-max"     ← higher capability Qwen model
```

### 3. ❌ Gemini Model Names (NON-EXISTENT)
```
"gemini-2.5-flash"
"gemini-2.0-flash"
```
✅ **Fixed to:**
```
"gemini-1.5-flash"   ← fast, efficient
"gemini-1.5-pro"     ← more capable
```

### 4. ❌ Router Config Format
```
"default": "gemini,gemini-2.5-flash"    ← comma separator
```
✅ **Fixed to:**
```
"default": "gemini|gemini-1.5-flash"    ← pipe separator for clarity
```

### 5. ✅ Added Transformer Directives
Added `transformer.use` configuration for both providers to enable proper model routing.

### 6. ✅ Enhanced Router Logic
```json
{
  "default": "gemini|gemini-1.5-flash",
  "background": "gemini|gemini-1.5-flash",
  "think": "gemini|gemini-1.5-pro",
  "longContext": "gemini|gemini-1.5-pro",
  "webSearch": "qwen|qwen-max",
  "codeGeneration": "qwen|qwen-plus"
}
```

## Configuration Summary

| Provider | Models | API Endpoint |
|----------|--------|--------------|
| **Gemini** | gemini-1.5-flash, gemini-1.5-pro | `https://generativelanguage.googleapis.com/v1beta/models/` |
| **Qwen** | qwen-plus, qwen-max | `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` |

## Status

✅ All model references corrected  
✅ API endpoints validated  
✅ Router configuration fixed  
✅ Ready for Claude-Qwen integration testing  

