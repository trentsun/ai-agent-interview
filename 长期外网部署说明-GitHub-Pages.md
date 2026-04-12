# 长期外网部署说明（GitHub Pages）

## 已经配好的内容

当前仓库已经加入：

- `site/` 静态网页产物
- `build_interview_site.py`：构建网页与 PDF
- `refresh_interview_site.sh`：本地一键刷新
- `.github/workflows/deploy-pages.yml`：GitHub Pages 自动部署工作流
- `requirements-deploy.txt`：GitHub Actions 依赖

## 部署效果

推到 GitHub 后，将自动实现：

1. `push` 到 `master` / `main` 时自动更新站点
2. 可在 Actions 页面手动触发更新
3. 每天自动抓取最新牛客面经并重建页面
4. 生成长期可访问的 GitHub Pages 链接

## 你现在只差最后 4 步

### 1. 在 GitHub 创建一个仓库

建议仓库名：

- `ai-interview-dashboard`
- 或 `nowcoder-ai-interview-dashboard`

### 2. 把本地仓库推上去

示例：

```bash
cd /Users/hilloworld/workspace/do_something/interview

git remote add origin <你的仓库URL>
git push -u origin master
```

如果你想改成 `main` 分支，也可以：

```bash
git branch -M main
git push -u origin main
```

### 3. 在 GitHub 仓库里打开 Pages

路径：

- `Settings` → `Pages` → `Build and deployment` → `Source` 选择 **GitHub Actions**

### 4. 等待 Actions 首次跑完

成功后，Pages 地址通常会是：

```text
https://<你的GitHub用户名>.github.io/<仓库名>/
```

## 注意事项

- GitHub Actions 的 `schedule` 任务只会在**默认分支**上执行。
- GitHub 文档说明：**公共仓库如果 60 天没有活动，scheduled workflow 会自动禁用**；后续重新 push 一次或手动启用即可。
- 如果仓库是私有仓库，GitHub Pages 是否可用取决于你的 GitHub 账户套餐。
- 当前站点内容是公开发布的，不要把敏感信息放进网页内容。

## 推荐做法

如果你只是要一个稳定的长期外网访问地址，优先用 GitHub Pages。

优点：

- 免费
- 稳定
- 静态站点很适合
- 自动更新链路简单

如果你后面还想挂**自定义域名**，可以再加：

- GitHub Pages + 自定义域名
- 或 Cloudflare 托管域名做反向接入
