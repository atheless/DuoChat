# `createPopup`

Creates a popup picker.

```javascript
import { createPopup } from '@picmo/popup-picker';
```

<pre>
  createPopup(pickerOptions: <a href="../../picmo/types/picker-options">PickerOptions</a>,
    popupOptions: <a href="../types/popup-options">PopupOptions</a>
  ): <a href="../classes/popup-picker-controller">PopupPickerController</a>
</pre>

Creates a popup emoji picker to be triggered by another element, usually a button.

## Arguments

### `pickerOptions`

Type: `Partial<`[`PickerOptions`](../../picmo/types/picker-options)`>`

The options to use when creating the popup picker.

:::note
When creating a popup picker, the [`autoFocus`](../../picmo/types/picker-options#autofocus) picker option deaults to `auto` so that the picker receives focus as soon as it is opened. This differs from an inline PicMo picker, which defaults to `none`.
:::

### `popupOptions`

Type: `Partial<`[`PickerOptions`](../types/popup-options)`>`

The options to use when creating the popup picker.

## Return value

The `PopupPickerController` instance that was created.
