--- .dev/releases/current/freshness-system/artifacts/D-0010/before.json	2026-05-12 19:53:53.332216726 +0000
+++ .dev/releases/current/freshness-system/artifacts/D-0010/after.json	2026-05-12 19:54:09.191610105 +0000
@@ -9,6 +9,89 @@
             "timeout": 10
           }
         ]
+      },
+      {
+        "matcher": "*",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-session-start.sh",
+            "timeout": 5
+          }
+        ]
+      }
+    ],
+    "UserPromptSubmit": [
+      {
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-user-prompt.sh",
+            "timeout": 3
+          }
+        ]
+      }
+    ],
+    "PreToolUse": [
+      {
+        "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-pre-edit.sh",
+            "timeout": 1
+          }
+        ]
+      }
+    ],
+    "PostToolUse": [
+      {
+        "matcher": "Read",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-post-read.sh",
+            "timeout": 1,
+            "async": true
+          }
+        ]
+      }
+    ],
+    "FileChanged": [
+      {
+        "matcher": ".*",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-file-changed.sh",
+            "timeout": 1,
+            "async": true
+          }
+        ]
+      }
+    ],
+    "SubagentStart": [
+      {
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-subagent-start.sh",
+            "timeout": 1,
+            "async": true
+          }
+        ]
+      }
+    ],
+    "SubagentStop": [
+      {
+        "hooks": [
+          {
+            "type": "command",
+            "command": "~/.claude/hooks/freshness-subagent-stop.sh",
+            "timeout": 1,
+            "async": true
+          }
+        ]
       }
     ]
   }
