# 4AFitment Vehicle Dropdown Scraper

这个小项目用于从 `https://car.4afitment.com/search/vc` 遍历车型兼容搜索页里的下拉列表：

- 年份范围固定选择 `1896` 到 `2027`
- 遍历制造商 / 品牌
- 嵌套遍历车型
- 每个组合点击搜索
- 点击“复制车型数据”
- 把复制出来的内容追加保存为 Markdown

它不会把账号密码写进代码。第一次运行登录脚本时，会打开浏览器，你手动登录后按回车，项目会把登录状态保存在本机 `.auth/profile` 目录里。

## 使用

在 PowerShell 里进入项目目录：

```powershell
cd D:\Home\Scripts\fitment_sheet_generation\4Afitment\fitment_sheet_generation
```

第一次先登录：

```powershell
.\run.ps1 src/login.js
```

浏览器打开后手动登录 4AFitment。登录完成并能看到车辆兼容搜索页后，回到 PowerShell 按回车。

然后开始抓取：

```powershell
.\run.ps1 src/scrape.js
```

结果会输出到：

- `output/fitment_data.md`
- `output/checkpoint.json`
- `output/network.jsonl`

## 按 TSV 清单抓取

把输入文件放到：

```text
input\carlist.tsv
```

支持两种格式：

```tsv
make
Acura
BMW
```

只有品牌列时，会遍历该品牌下的所有车型。

```tsv
make	model
Acura	MDX
BMW	X5
```

有品牌和车型两列时，只抓取指定组合。列名也兼容 `brand`、`manufacturer`、`品牌`、`model`、`车型`。

运行：

```powershell
.\run.ps1 src/scrape-from-tsv.js
```

结果会输出到：

- `output/from_tsv.md`
- `output/from_tsv_summary.md`
- `output/from_tsv_checkpoint.json`

找不到的品牌或车型会写在 `output/from_tsv_summary.md` 里说明原因。

## 如果页面控件识别不准

先运行检查脚本：

```powershell
.\run.ps1 src/inspect.js
```

它会把页面上疑似下拉控件打印出来。你可以把更准确的 CSS 选择器填到 `config.json`：

```json
{
  "selectors": {
    "yearFrom": ["select[name='year_from']"],
    "yearTo": ["select[name='year_to']"],
    "manufacturer": ["select[name='make']"],
    "model": ["select[name='model']"],
    "searchButton": ["button[type='submit']"],
    "copyButton": ["button:has-text('复制车型数据')"]
  }
}
```

脚本会优先使用这里写好的选择器；没有填写时，会按标签文字、placeholder、name、id、aria-label 自动猜测。

## 断点续跑

抓取过程中会持续写 `output/checkpoint.json`。如果中断，再运行 `src/scrape.js` 会跳过已经复制过的制造商 / 车型组合。

## 说明

4AFitment 页面通常需要登录。如果登录过期，重新运行登录脚本即可。
