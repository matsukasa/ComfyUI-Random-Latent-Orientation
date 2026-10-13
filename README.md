# Random Latent Orientation

ComfyUI の `LATENT` を受け取り、指定した確率で縦横を入れ替えるカスタムノードです。
入力 LATENT のサイズを自動取得するため、幅や高さを入力し直す必要はありません。

## インストール

このフォルダを ComfyUI の `custom_nodes` フォルダへ配置し、ComfyUI を再起動してください。

```text
ComfyUI/
└─ custom_nodes/
   └─ ComfyUI-Random-Latent-Orientation/
      ├─ __init__.py
      └─ nodes.py
```

外部カスタムノードや追加ライブラリへの依存はありません。

## 入出力

ノード名は **Random Latent Orientation**、カテゴリは `latent` です。

| 種類 | 名前 | 内容 |
| --- | --- | --- |
| 入力 | `latent` | 必須の `LATENT` |
| 入力 | `swap_probability` | 縦横を交換する確率。0〜100、初期値50、1刻み |
| 出力 | `latent` | 縦横交換後、または元の `LATENT` |

## 確率設定

- `0`：常に縦横を維持します。
- `100`：正方形でない場合、常に縦横を交換します。
- `50`：50%の確率で縦横を交換します。

同じワークフローをキューに再投入した場合も、その都度ランダム判定を行います。
不要なシード入力はありません。

## 使用例

`Empty Latent Image` と `KSampler` の間に接続します。

```text
Empty Latent Image
        ↓
Random Latent Orientation
        ↓
KSampler
```

例えば 832×1216 の LATENT は、交換時に 1216×832 になります。
1024×1024 のように縦横が等しい場合は、確率設定に関係なく変更しません。

## 注意事項

- 画像の回転やリサイズではなく、LATENT テンソルの Height / Width 次元を交換します。
- Batch と Channels、テンソルの device と dtype は変更しません。
- ピクセル数とバッチ数は変更しません。
- 入力 LATENT は破壊的に変更しません。
- `noise_mask` がある場合は、その空間次元も同じように交換します。
- その他のメタデータは保持します。
- 入力 `samples` は `[B, C, H, W]` の4次元テンソルである必要があります。
