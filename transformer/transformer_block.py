import numpy as np


class TransformerDecoderBlock:
    def __init__(
        self,
        X,
        Wq=None,
        Wk=None,
        Wv=None,
        Wo=None,
        W1=None,
        W2=None,
        b1=None,
        b2=None,
        batch_size=1,
        d_model=1024,
    ):
        """
        X: 输入数据，维度为[batch_size, seq_len, d_model]
        Wq: 查询权重，维度为[d_model, d_model]
        Wk: 键权重，维度为[d_model, d_model]
        Wv: 值权重，维度为[d_model, d_model]
        Wo: 输出权重，维度为[d_model, d_model]
        W1: 第一层线性变换权重，维度为[d_model, d_model]
        W2: 第二层线性变换权重，维度为[d_model, d_model]
        compute_mode: 计算模式，'prefill'或'decode'
        """
        self.X = X
        self.M = self.init_mask()
        self.batch_size = batch_size
        self.seq_len = X.shape[1]
        self.d_model = d_model
        self.Wq = Wq
        self.Wk = Wk
        self.Wv = Wv
        self.Wo = Wo
        self.W1 = W1
        self.W2 = W2
        self.b1 = b1
        self.b2 = b2
        self.K = None
        self.V = None
        # 模拟初始化权重
        self.init_weights()
        # 校验输入的维度和权重
        self.check_input_dim()
        self.check_weights()

    def init_mask(self):
        """
        初始化掩码，维度为[batch_size, seq_len, seq_len]
        """
        M = np.zeros((self.batch_size, self.seq_len, self.seq_len), dtype=np.float32)
        np.fill_diagonal(M, -float('inf'))
        return M

    def init_weights(self):
        """
        初始化权重
        """
        if self.Wq is None:
            self.Wq = np.random.randn(self.d_model, self.d_model)
        if self.Wk is None:
            self.Wk = np.random.randn(self.d_model, self.d_model)
        if self.Wv is None:
            self.Wv = np.random.randn(self.d_model, self.d_model)
        if self.Wo is None:
            self.Wo = np.random.randn(self.d_model, self.d_model)
        if self.W1 is None:
            self.W1 = np.random.randn(self.d_model, self.d_model)
        if self.W2 is None:
            self.W2 = np.random.randn(self.d_model, self.d_model)
        if self.b1 is None:
            self.b1 = np.zeros(self.d_model)
        if self.b2 is None:
            self.b2 = np.zeros(self.d_model)

    def check_input_dim(self):
        """
        校验输入的维度
        """
        if self.X.shape[0] != self.batch_size:
            raise ValueError(
                f"输入的batch_size与初始化的batch_size不一致，输入的batch_size为{self.X.shape[0]}，初始化的batch_size为{self.batch_size}"
            )
        if self.X.shape[2] != self.d_model:
            raise ValueError(
                f"输入的d_model与初始化的d_model不一致，输入的d_model为{self.X.shape[2]}，初始化的d_model为{self.d_model}"
            )
        if self.Wq.shape[0] != self.d_model or self.Wq.shape[1] != self.d_model:
            raise ValueError(
                f"输入的Wq的维度与初始化的d_model不一致，输入的Wq的维度为{self.Wq.shape}，初始化的d_model为{self.d_model}"
            )
        if self.Wk.shape[0] != self.d_model or self.Wk.shape[1] != self.d_model:
            raise ValueError(
                f"输入的Wk的维度与初始化的d_model不一致，输入的Wk的维度为{self.Wk.shape}，初始化的d_model为{self.d_model}"
            )
        if self.Wv.shape[0] != self.d_model or self.Wv.shape[1] != self.d_model:
            raise ValueError(
                f"输入的Wv的维度与初始化的d_model不一致，输入的Wv的维度为{self.Wv.shape}，初始化的d_model为{self.d_model}"
            )
        if self.Wo.shape[0] != self.d_model or self.Wo.shape[1] != self.d_model:
            raise ValueError(
                f"输入的Wo的维度与初始化的d_model不一致，输入的Wo的维度为{self.Wo.shape}，初始化的d_model为{self.d_model}"
            )
        if self.W1.shape[0] != self.d_model or self.W1.shape[1] != self.d_model:
            raise ValueError(
                f"输入的W1的维度与初始化的d_model不一致，输入的W1的维度为{self.W1.shape}，初始化的d_model为{self.d_model}"
            )
        if self.W2.shape[0] != self.d_model or self.W2.shape[1] != self.d_model:
            raise ValueError(
                f"输入的W2的维度与初始化的d_model不一致，输入的W2的维度为{self.W2.shape}，初始化的d_model为{self.d_model}"
            )
        if self.b1.shape[0] != self.d_model:
            raise ValueError(
                f"输入的b1的维度与初始化的d_model不一致，输入的b1的维度为{self.b1.shape}，初始化的d_model为{self.d_model}"
            )
        if self.b2.shape[0] != self.d_model:
            raise ValueError(
                f"输入的b2的维度与初始化的d_model不一致，输入的b2的维度为{self.b2.shape}，初始化的d_model为{self.d_model}"
            )

    def softmax(self, x):
        x = x - np.max(x, axis=-1, keepdims=True)
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    def gelu(self, x):
        # 近似实现 (Gaussian Error Linear Unit)
        return (
            0.5
            * x
            * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * np.power(x, 3))))
        )

    def layer_norm(self, x, eps=1e-5):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return (x - mean) / np.sqrt(var + eps)

    def forward(self):
        #################################
        # 1. Self-Attention 自注意力子层 #
        #################################
        # 1.1 LayerNorm归一化
        x = self.layer_norm(self.X)
        # 1.2 计算attention
        Q = np.dot(x, self.Wq)
        K = np.dot(x, self.Wk)
        V = np.dot(x, self.Wv)
        attn_scores = np.dot(Q, K.T) / np.sqrt(Q.shape[-1]) + self.M
        attn_probs = self.softmax(attn_scores)
        A = np.dot(attn_probs, V)
        O = np.dot(A, self.Wo)
        # 1.3 ResidualAdd 残差连接相加
        X1 = self.X + O
        ##########################################
        #  2. FeedForwardNetwork 前馈神经网络子层  #
        ##########################################
        # 2.1 LayerNorm归一化
        x = self.layer_norm(X1)
        # 2.2 计算FFN
        O1 = np.dot(x, self.W1) + self.b1
        hidden = self.gelu(O1)
        O2 = np.dot(hidden, self.W2) + self.b2
        # 2.3 ResidualAdd 残差连接相加
        X2 = X1 + O2
        return X2
