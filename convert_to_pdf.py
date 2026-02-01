import os
import img2pdf
from PIL import Image

def convert_images_to_pdf(source_folder, output_folder):
    """
    读取指定文件夹中的图片，将其转换为PDF格式并保存到目标文件夹。
    
    参数:
        source_folder (str): 图片文件的源目录路径
        output_folder (str): 生成的PDF文件的保存目录路径
    """
    
    # 检查源目录是否存在
    if not os.path.exists(source_folder):
        print(f"错误: 源文件夹 '{source_folder}' 不存在。")
        return

    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"已创建输出文件夹: {output_folder}")
        except OSError as e:
            print(f"创建输出文件夹失败: {e}")
            return

    # 获取文件夹中所有图片文件的列表
    # 过滤条件: 以 .png, .jpg, .jpeg 结尾的文件 (不区分大小写)
    image_files = [
        os.path.join(source_folder, i)
        for i in os.listdir(source_folder)
        if i.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]

    # 遍历所有图片文件，并单独将每张图片转换为PDF
    if image_files:
        converted_count = 0
        print(f"在 '{source_folder}' 中找到 {len(image_files)} 张图片，开始转换...")
        
        for image_file in image_files:
            try:
                # ---------------------------------------------------------
                # 1. 准备输出路径
                # ---------------------------------------------------------
                # 获取文件名（不带路径）
                base_name = os.path.basename(image_file)
                # 去除扩展名，并添加 .pdf 后缀
                pdf_filename = os.path.splitext(base_name)[0] + ".pdf"
                # 组合完整的目标路径
                pdf_path = os.path.join(output_folder, pdf_filename)
                
                # ---------------------------------------------------------
                # 2. 计算图片尺寸和 DPI (每英寸点数)
                # ---------------------------------------------------------
                # 使用 Pillow 打开图片以获取其物理尺寸和分辨率信息
                with Image.open(image_file) as img:
                    width_px, height_px = img.size
                    dpi_info = img.info.get('dpi')
                    
                    if dpi_info:
                        # 如果图片包含 DPI 信息，根据 DPI 计算 PDF 中的点(point)尺寸
                        # PDF 标准中 1 inch = 72 points
                        # 公式: 尺寸(pt) = 像素(px) * 72 / DPI
                        width_pt = width_px * 72 / dpi_info[0]
                        height_pt = height_px * 72 / dpi_info[1]
                    else:
                        # 如果没有 DPI 信息，默认 DPI 为 72
                        # 此时 1 pixel = 1 point，保持 1:1 映射
                        width_pt, height_pt = width_px, height_px

                # ---------------------------------------------------------
                # 3. 转换并保存 PDF
                # ---------------------------------------------------------
                # 创建一个布局函数 (layout function)，指定 PDF页面的确切大小 (width_pt, height_pt)
                # 这确保了生成的 PDF 页面尺寸与图片的物理尺寸完全匹配，不会被缩放或留白
                layout_fun = img2pdf.get_layout_fun((width_pt, height_pt))

                # 将图片数据转换为 PDF 字节流并写入文件
                with open(pdf_path, "wb") as f:
                    f.write(img2pdf.convert(image_file, layout_fun=layout_fun))
                
                print(f"成功: {base_name} -> {pdf_filename}")
                converted_count += 1
                
            except Exception as e:
                print(f"失败: 转换 {image_file} 时出错。原因: {e}")
        
        print(f"\n处理完成。总共成功转换了 {converted_count} 张图片。")
        print(f"所有 PDF 文件已保存至: {os.path.abspath(output_folder)}")
    else:
        print(f"在当前目录下没有找到任何图片文件 (.png, .jpg, .jpeg)。")

def main():
    """
    主测试函数
    可以在这里修改 source_dir 和 output_dir 来测试不同的路径。
    """
    # 设定源图片路径 (默认为当前脚本所在目录)
    source_dir = './src_img'
    
    # 设定目标PDF保存路径 
    # 这里为了演示，将其保存到当前目录下的 'pdf_output' 子文件夹中，避免与源文件混淆
    # 如果你想保存在当前目录，可以将 output_dir 设置为 '.'
    output_dir = './dst_img' 
    
    print("=== 图片转 PDF 脚本启动 ===")
    convert_images_to_pdf(source_dir, output_dir)

if __name__ == "__main__":
    main()
