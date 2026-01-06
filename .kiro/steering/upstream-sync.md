# Syncing with Upstream AWS Agent Evaluation

This repository is a fork of the official AWS agent-evaluation framework with Shopify-specific extensions.

## Current Git Configuration

✅ **Origin**: `https://github.com/chrissandico/agent-evaluation.git` (your fork)
✅ **Upstream**: `https://github.com/awslabs/agent-evaluation.git` (official AWS repo)

## Repository Structure

```
Your Fork (origin)
    ↓ pull/push
Your Local Repo
    ↓ fetch/merge
Official AWS Repo (upstream)
```

## Syncing with Upstream

### Check for Updates

```bash
# Fetch latest changes from upstream
git fetch upstream

# View what's new
git log HEAD..upstream/main --oneline
```

### Pull Latest Changes

```bash
# Make sure you're on main branch
git checkout main

# Fetch and merge upstream changes
git fetch upstream
git merge upstream/main

# Or use rebase to keep history clean
git rebase upstream/main
```

### Push Updates to Your Fork

```bash
# Push merged changes to your fork
git push origin main
```

## Handling Conflicts with Shopify Extensions

Your Shopify-specific files should NOT conflict with upstream:

### Safe Files (Won't Conflict)
- `shopify_extensions/` - Your custom code
- `.kiro/steering/` - Your steering rules
- `agenteval.yml` - Your test configuration
- Shopify-specific test files

### Files That May Conflict
- `src/agenteval/` - Core framework code
- `requirements.txt` - Dependencies
- `setup.py` - Package configuration
- `docs/` - Documentation

### Resolving Conflicts

If conflicts occur during merge:

```bash
# View conflicted files
git status

# For each conflict:
# 1. Open the file and resolve conflicts manually
# 2. Keep upstream changes for core framework
# 3. Keep your changes for Shopify extensions

# After resolving:
git add <resolved-file>
git commit
```

## Recommended Workflow

### 1. Regular Sync Schedule

Sync with upstream weekly or before major work:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 2. Work on Feature Branches

Keep main clean and work on branches:

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/my-shopify-enhancement

# Make changes, commit, push
git push origin feature/my-shopify-enhancement
```

### 3. Update Dependencies

After syncing, update Python packages:

```bash
# Check for requirement changes
git diff upstream/main requirements.txt

# Reinstall if needed
pip install -e ".[dev]"
```

### 4. Test After Sync

Always test after pulling upstream changes:

```bash
# Run linting
flake8 src/ && black --check src/ && isort src/ --check --diff

# Run tests
python -m pytest .

# Test CLI
agenteval --help

# Test Shopify integration
python simple_final_test.py
```

## Keeping Shopify Extensions Compatible

### When Upstream Changes Core Framework

1. **Check breaking changes** in upstream CHANGELOG.md
2. **Update Shopify target** if BaseTarget interface changes
3. **Test thoroughly** with your Shopify agent
4. **Update documentation** if needed

### Example: BaseTarget API Change

If upstream changes `BaseTarget.invoke()` signature:

```bash
# Check what changed
git diff upstream/main src/agenteval/targets/

# Update your Shopify target
# Edit: shopify_extensions/targets/shopify_agent_target.py

# Test the changes
python -c "from shopify_extensions.targets.shopify_agent_target import ShopifyAgentTarget; print('OK')"
```

## Version Tracking

### Check Upstream Version

```bash
# View upstream version
git fetch upstream
git show upstream/main:setup.py | grep VERSION
```

### Check Your Version

```bash
# View your version
grep VERSION setup.py
```

### Update Version After Sync

If you sync major upstream changes, document in your fork:

```bash
# Tag your synced version
git tag -a v0.4.1-shopify-1 -m "Synced with upstream v0.4.1, Shopify extensions v1"
git push origin v0.4.1-shopify-1
```

## Emergency: Reset to Upstream

If your fork gets too diverged and you want to reset:

```bash
# CAUTION: This will lose your changes!
# Backup Shopify extensions first
cp -r shopify_extensions/ ../shopify_extensions_backup/

# Reset to upstream
git fetch upstream
git checkout main
git reset --hard upstream/main

# Restore Shopify extensions
cp -r ../shopify_extensions_backup/ shopify_extensions/

# Commit and push
git add shopify_extensions/
git commit -m "chore: restore Shopify extensions after upstream reset"
git push origin main --force
```

## Best Practices

1. **Sync regularly** - Don't let your fork get too far behind
2. **Keep extensions separate** - All Shopify code in `shopify_extensions/`
3. **Don't modify core** - Avoid changing `src/agenteval/` unless absolutely necessary
4. **Test after sync** - Always run tests after pulling upstream
5. **Document changes** - Note any compatibility updates needed
6. **Use branches** - Keep main clean, work on feature branches
7. **Tag releases** - Tag stable versions of your Shopify integration

## Quick Reference

```bash
# Daily workflow
git fetch upstream                    # Check for updates
git log HEAD..upstream/main --oneline # See what's new

# Weekly sync
git checkout main
git fetch upstream
git merge upstream/main
pip install -e ".[dev]"
python -m pytest .
git push origin main

# Before major work
git fetch upstream
git checkout main
git merge upstream/main
git checkout -b feature/my-work
```

## Troubleshooting

### "Already up to date" but versions differ

```bash
git fetch upstream --tags
git log --oneline --graph --all
```

### Merge conflicts in src/

```bash
# Accept upstream version for core framework
git checkout --theirs src/agenteval/
git add src/agenteval/
```

### Shopify target breaks after sync

```bash
# Check BaseTarget changes
git diff HEAD~1 src/agenteval/targets/

# Review official target examples
# Visit: https://awslabs.github.io/agent-evaluation/targets/
```
