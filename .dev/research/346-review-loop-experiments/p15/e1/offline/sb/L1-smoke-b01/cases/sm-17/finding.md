### R1-1 Exports are written to a shared directory
Both export rules write files to one shared directory, so the files of different tenants sit side by side and can be read by anyone who can read the directory. Cited: spec lines 32-34 (before version).
An implementer who follows EX-3 and EX-4 builds exports that every tenant can read because all files share one directory.
Protected requirement: line 32 (tenant isolation must hold).
