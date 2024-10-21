#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   add_pinyin.py
@Time    :   2024/10/21 14:40:46
@Author  :   Ferret@NJTech 
@Version :   1.0
@Contact :   Ferret@NJTech
@License :   (C)Copyright 2024, Ferret@NJTech
@Desc    :   补充描述 
'''

from datetime import datetime
import logging
import pathlib
from PIL import Image, ImageDraw, ImageFont

START = datetime.now()
thisScript = pathlib.Path(__file__)
root = thisScript.parent
logLevel = logging.INFO
logFile = thisScript.with_suffix('.log')


# fmt:off
# Basic logging configuration
logging.basicConfig(
    level=logLevel,
    format='%(message)s' if logLevel == logging.INFO else '%(asctime)s %(filename)s(%(lineno)04d) [%(levelname)-8s]: %(message)s',
    handlers=[logging.FileHandler(logFile, mode='w', encoding='utf-8'), logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S'
)
# fmt:on


def image_add_text(img, text, left, top, text_color=(255, 0, 0), text_size=13):
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式 这里的SimHei.ttf需要有这个字体
    fontStyle = ImageFont.truetype(root.joinpath("FangZhengKaiTiPinYinZiKu-1.ttc"), text_size, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, text_color, font=fontStyle)
    width = fontStyle.getlength(text)
    logging.info(f'width={width}')
    # draw.rectangle([xPos,yPos,xPos+width,yPos+text_size],fill=None,outline=text_color,width=1)
    return img


def load_image(img_path):
    img = Image.open(img_path)
    return img


def save_image(img, img_path):
    img.save(img_path)


def _tuple_add(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))


# fmt:off
def patch_image(img, src=(345, 520), src_size=(10, 10), 
                dst_xPos=355, dst_yPos=520, dst_size=(580, 180),
                yPos1=0, yPos2=0):
# fmt:on    
    # 首先使用背景色覆盖原文字
    part = img.copy()
    # src = (src_xPos, src_yPos)
    crop_region = src + _tuple_add(src, src_size)
    # logging.info(crop_region)
    dst = (dst_xPos, dst_yPos)
    background = part.crop(crop_region).resize(dst_size)
    paste_region = dst + _tuple_add(dst, dst_size)
    # logging.info(paste_region)
    img.paste(background, paste_region)

    pos, size = (125, yPos2), (875, 40)
    move_regin = pos + _tuple_add(pos, size)
    logging.info(move_regin)
    # draw = ImageDraw.Draw(img)
    # draw.rectangle(move_regin, fill=None, outline='#4DB2E6', width=3)

    # 下移 自我评价部分
    moved = part.crop(move_regin)
    background = background.resize(moved.size)
    img.paste(background, move_regin)

    move_pos = _tuple_add(pos, (0, 55))
    img.paste(moved, move_pos + _tuple_add(move_pos, size))
    # crop_region =

    return img


image_data = {
    'week03': {'words': '如鱼得水 一石二鸟 杯弓蛇影 亡羊补牢 画龙点睛 老马识途', 'pos1': 475, 'pos2': 615},
    'week04': {'words': '万紫千红 花红柳绿 白雪皑皑 五颜六色 五光十色 五彩缤纷', 'pos1': 490, 'pos2': 625},
    'week05': {'words': '繁花似锦 花团锦簇 百花齐放 郁郁葱葱 枝繁叶茂 绿草如茵', 'pos1': 453, 'pos2': 600},
    'week06': {'words': '白雪皑皑 冰天雪地 天寒地冻 滴水成冰 鹅毛大雪 风雪交加', 'pos1': 480, 'pos2': 620},
    'week07': {'words': '水天一色 高耸入云 湖光山色 青山绿水 别有洞天 山清水秀', 'pos1': 515, 'pos2': 652},
}


# 所有图片缩放为 (1280, 1240)
def main():
    suffixs = ['.jpg', '.png']
    images = [p for p in root.joinpath('images').glob('*') if p.is_file() and p.suffix in suffixs]

    for image in images:
        im = load_image(image)
        logging.info(f"{image.name}: {im.size}")
        # if im.size != (1280,1024):
        if im.size[0] != (1280):
            im = im.resize((1280, 1240))
        data = image_data[image.stem]

        words = [w for w in data['words'].split() if w]
        yPos1 = data['pos1']
        yPos2 = data['pos2']
        im = patch_image(im, dst_yPos=yPos1, yPos2=yPos2)
        im = image_add_text(im, " ".join(words[:3]), 225, yPos1, text_color='#353439', text_size=65)
        im = image_add_text(im, " ".join(words[3:]), 225, yPos1 + 100, text_color='#353439', text_size=65)
        save_image(im, root.joinpath('results',f'add_{image.name}'))


if __name__ == '__main__':
    # fmt: off
    logging.info('脚本 %s 开始运行, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    logging.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
