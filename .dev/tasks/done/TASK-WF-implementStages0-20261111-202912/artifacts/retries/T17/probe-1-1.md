0f6bc94ef61d927be950167aa9e21f8393183afb
Family probe publish-precheck / init-resume-identity: other writers in manifest.py: save() (atomic, writes only the manifest), commit_published (advance_stage then save), CLI advance --publish-from (goes through publish_files). resume() callers: manifest_cmd init only. No other instance.
