frame = GlassFrame()
frame.setFixedSize(300, 200)

# 通过QSS设置扩展属性
frame.setStyleSheet("""
    GlassFrame {
        qproperty-gradientAngle: 45;
        qproperty-borderColor: rgba(200, 220, 255, 150);
        qproperty-shadowColor: rgba(100, 120, 150, 80);
        qproperty-shadowBlur: 40;
        qproperty-hoverAnimDuration: 500;
        qproperty-glassOpacity: 0.25;
    }
""")

# 动态修改动画参数
frame.hoverEasingCurve = QEasingCurve.OutBack  # 弹性效果
frame.gradientAngle = 90  # 垂直渐变

# 添加点击动画
def animate_click():
    angle_anim = QPropertyAnimation(frame, b"gradientAngle")
    angle_anim.setDuration(500)
    angle_anim.setStartValue(frame.gradientAngle)
    angle_anim.setEndValue(frame.gradientAngle + 180)
    angle_anim.setEasingCurve(QEasingCurve.InOutQuad)
    angle_anim.start()

frame.mousePressEvent = lambda e: animate_click()

# 创建高级玻璃效果
advanced_frame = GlassFrame()
advanced_frame.setStyleSheet("""
    GlassFrame {
        /* 基础样式 */
        qproperty-borderRadius: 24;
        qproperty-borderWidth: 2;
        qproperty-glassOpacity: 0.3;

        /* 渐变控制 */
        qproperty-backgroundGradient: [
            rgba(255, 255, 255, 0.4),
            rgba(200, 220, 255, 0.2)
        ];
        qproperty-gradientAngle: 135;

        /* 阴影设置 */
        qproperty-shadowColor: rgba(50, 70, 120, 60);
        qproperty-shadowBlur: 50;

        /* 悬停动画参数 */
        qproperty-hoverAnimDuration: 400;
        qproperty-hoverEasingCurve: OutBack;
    }

    /* 子元素样式 */
    QLabel#content {
        color: white;
        font: 16px "Segoe UI";
        padding: 24px;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 12px;
    }
""")

# 禁用阴影动画
frame.hover_anim_group.removeAnimation(frame.shadow_anim)


# 自定义悬停效果
def custom_hover_effect(enter):
    if enter:
        anim = QPropertyAnimation(frame, b"gradientAngle")
        anim.setStartValue(frame.gradientAngle)
        anim.setEndValue(frame.gradientAngle + 30)
        anim.start()


frame.hoverEffectEnabled = False  # 禁用默认动画
frame.enterEvent = lambda e: custom_hover_effect(True)
frame.leaveEvent = lambda e: custom_hover_effect(False)
