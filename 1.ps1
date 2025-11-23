# === 配置区 ===
$ModelName = "kandinsky-community/kandinsky-2-2-prior"               # 替换为你下载的模型名（ModelScope 和 HF 名称需一致）
$LocalModelDir = "C:\Users\Administrator\.cache\modelscope\hub\models\kandinsky-community\kandinsky-2-2-prior"      # 替换为你实际下载好的 ModelScope 模型路径
$HFHome = if ($env:HF_HOME) { $env:HF_HOME } else { "$env:USERPROFILE\.cache\huggingface" }

# === 自动构建 HF 路径 ===
$HFModelName = $ModelName.Replace("/", "--")
$HFDir = Join-Path $HFHome "hub" "models--$HFModelName"

Write-Host "目标 HF 目录: $HFDir"

# === 获取 HF 上该模型的最新 commit hash ===
# 注意：此步骤需要能访问 huggingface.co（即使只是获取 HEAD hash）
try {
    $GitUrl = "https://huggingface.co/$ModelName"
    $Response = Invoke-RestMethod -Uri "$GitUrl/info/refs?service=git-upload-pack"
    # 提取第一个 commit hash（通常是 HEAD）
    $CommitHash = ($Response -split "`n" | Where-Object { $_ -match '^[0-9a-f]{40}' } | Select-Object -First 1).Substring(0, 40)
} catch {
    Write-Warning "无法从 Hugging Face 获取 commit hash，尝试使用默认值或手动指定。"
    # 如果无法联网，可手动设置一个任意 hash（只要目录名一致即可）
    $CommitHash = "main"  # 或者用固定值如 "dummyhash1234567890"
}

if (-not $CommitHash) {
    $CommitHash = "main"
}

Write-Host "使用的 commit hash: $CommitHash"

# === 创建 HF 所需目录结构 ===
$SnapshotDir = Join-Path $HFDir "snapshots" $CommitHash
$RefsDir = Join-Path $HFDir "refs"

if (-not (Test-Path $SnapshotDir)) {
    New-Item -ItemType Directory -Path $SnapshotDir -Force | Out-Null
}
if (-not (Test-Path $RefsDir)) {
    New-Item -ItemType Directory -Path $RefsDir -Force | Out-Null
}

# === 移动或复制模型文件到 snapshots/<hash>/ ===
# 注意：此处假设 $LocalModelDir 是你已下载的 ModelScope 模型根目录
Get-ChildItem -Path $LocalModelDir -File | ForEach-Object {
    Copy-Item $_.FullName -Destination $SnapshotDir -Force
}
Get-ChildItem -Path $LocalModelDir -Directory | ForEach-Object {
    Copy-Item $_.FullName -Destination $SnapshotDir -Recurse -Force
}

# === 写入 refs/main 文件 ===
Set-Content -Path (Join-Path $RefsDir "main") -Value $CommitHash

Write-Host "✅ 转换完成！现在你可以使用以下方式加载模型："
Write-Host "from transformers import AutoModel"
Write-Host "model = AutoModel.from_pretrained('$ModelName')"