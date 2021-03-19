import os
from libsite.producer import Producer
from libass.studio import Studio

INPUT_FILENAME = '1'
FILTER_FILE = 'D:\\Anime\\Tools\\xml2ass\\list.txt'
HEADER_FILE = 'D:\\Anime\\Tools\\xml2ass\\head.txt'

IO_CONFIG = {
    # 输入文件名
    'input_filename': INPUT_FILENAME + '.xml',
    # 输出文件名
    'output_filename': INPUT_FILENAME + '.ass'
}

DANMAKU_CONFIG = {
    # 过滤文件
    'custom_filter': FILTER_FILE,
    # 过滤底部弹幕
    'bottom_filter': True,
    # 过滤游客弹幕
    'guest_filter': True,
    # 过滤顶部弹幕
    'top_filter': False
}

SUBTITLE_CONFIG = {
    # 底部边距
    'bottom_margin': 0,
    # 自定义偏移
    'custom_offset': '00:00',
    # 丢弃偏移
    'drop_offset': 2,
    # 字体名称，默认None为自动选择
    'font_name': None,
    # 字体大小
    'font_size': 32,
    # 样式模板
    'header_file': HEADER_FILE,
    # 布局算法，可选'sync'和'async'
    'layout_algorithm': 'sync',
    # 限制行数
    'line_count': 0,
    # 播放分辨率
    'play_resolution': '1920x1080',
    # 微调时长
    'tune_duration': 1
}


def convert(io_args, danmaku_args, subtitle_args):
    input_filename = io_args['input_filename']
    output_filename = io_args['output_filename']

    # 弹幕预处理
    producer = Producer(danmaku_args, input_filename)
    producer.start_handle()
    print('屏蔽条数：游客(%(guest)d) + 顶部(%(top)d) + '
          '底部(%(bottom)d) + 自定义(%(custom)d) = %(blocked)d\n'
          '通过条数：总共(%(total)d) - 屏蔽(%(blocked)d) = %(passed)d' %
          producer.report())

    # 字幕生成
    danmakus = producer.keeped_danmakus
    studio = Studio(subtitle_args, danmakus)
    studio.start_handle()
    studio.create_ass_file(output_filename)
    print('字幕条数：总共(%(total)d) - 丢弃(%(droped)d) = %(keeped)d' % studio.report())
    print('字幕文件：%s' % os.path.basename(output_filename))


if __name__ == '__main__':
    convert(IO_CONFIG, DANMAKU_CONFIG, SUBTITLE_CONFIG)
