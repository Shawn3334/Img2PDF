# 图片转 PDF 工具

这是一个简单的 Python 脚本，用于将指定文件夹下的图片（jpg, png, jpeg, bmp）批量转换为 PDF 文件。

## 功能特点
- 保持图片的原始尺寸和比例
- 自动识别图片 DPI，确保打印尺寸正确
- 批量处理，生成同名 PDF 文件

## 环境要求

- Python 3.x
- 依赖库：见 `requirements.txt`

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行脚本**
   默认会将 ./src_img 下的图片转换为 ./dst_img 下的 PDF 文件。
   ```bash
   python convert_to_pdf.py
   ```

## 自定义路径
你可以修改 `convert_to_pdf.py` 文件底部的 `main` 函数来指定源文件夹和目标文件夹：

```python
def main():
    # 设定源图片路径
    source_dir = './src_img'
    
    # 设定目标PDF保存路径
    output_dir = './dst_img' 
    
    convert_images_to_pdf(source_dir, output_dir)
```
