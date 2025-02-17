import matplotlib.pyplot as plt

def line_chart(df_ada, df_dot, coin1="cardano", coin2="polkadot", price= "SEK"):
    fig, ax = plt.subplots(1)

    # 绘制第一个币种的曲线
    ax.plot(df_ada.index, df_ada[price], label=coin1, linewidth=2, color="blue")

    # 绘制第二个币种的曲线
    ax.plot(df_dot.index, df_dot[price], label=coin2, linewidth=2, color="orange")

    # 设置图表信息
    ax.set_title(f"Real-time Prices of {coin1} & {coin2}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()            # 自动调整子图布局，防止重叠
    return fig
 




"""
    在同一个折线图上绘制两种加密货币的价格走势。
    
    参数：
    - df_ada: DataFrame (Cardano 或其他币种)
    - df_dot: DataFrame (Polkadot 或其他币种)
    - coin1: str (第一个币种的名称)
    - coin2: str (第二个币种的名称)
    
    返回：
    - Matplotlib 图像对象
"""
















