import cv2
import numpy as np


def match_algorithm(template, full_img):
    """
    定位方式1：模板匹配
    """
    h, w = template.shape[:2]  # rows->h, cols->w
    img_gray = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)
    # 6种匹配方法
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    for meth in methods:
        # 匹配方法的真值
        method = eval(meth)
        res = cv2.matchTemplate(img_gray, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 如果是平方差匹配TM_SQDIFF或归一化平方差匹配TM_SQDIFF_NORMED，取最小值
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.circle(res, top_left, 10, 0, 2)
        return top_left


def hough_detect():
    """
    定位方式2：hough检测
    """
    pass


def similar_calculate(template, img):
    hash_grid = 16
    t_gray = cv2.cvtColor(cv2.resize(template, (hash_grid, hash_grid)), cv2.COLOR_BGR2GRAY)
    i_gray = cv2.cvtColor(cv2.resize(img, (hash_grid, hash_grid)), cv2.COLOR_BGR2GRAY)

    t_hash = np.where(t_gray > np.mean(t_gray), 1, 0).flatten()
    i_hash = np.where(i_gray > np.mean(i_gray), 1, 0).flatten()

    return 1-np.sum(t_hash ^ i_hash)/hash_grid**2


def calculate_distance():
    """
    测距用guide物应该为一个矩形物体，最好是正方形。
    F = λ（H/h）f
    F：物距 单位：cm
    λ：单位换算因子
    H:实物尺寸 单位：cm
    h:成像尺寸 单位：像素点
    f:焦距  单位：mm
    :return:
    """
    pass


def get_f():
    return 0.1


def generate_lambda():
    """
    λ = F / （H/h）f
    F：物距 单位：cm
    λ：单位换算因子
    H:实物尺寸 单位：cm
    h:成像尺寸 单位：像素点
    f:焦距  单位：mm
    :return:
    """
    f = get_f()
    F = 10
    H = 10
    h = 30

    return F / (H/h)*f


def main():
    img = cv2.imread('dog.jpg')
    template = cv2.imread('face_dog.jpg', 0)
    match_algorithm(template, img)


if __name__ == '__main__':
    cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.5.64:554/h264/ch1/main/av_stream")
    # write_cap = cv2.VideoWriter("3hao.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20.0, (1280, 720))
    while 1:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("frame", frame)
        # write_cap.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # write_cap.release()
    cap.release()