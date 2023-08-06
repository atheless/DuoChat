# `PopupOptions`

## Popup properties

### `className`

- **Type**: `string` | `undefined`

Sets any additional CSS classes to be applied to the popup container. This is typically used to override theme styles or to apply a custom `z-index`.

### `hideOnClickOutside`

- **Type**: `boolean`
- **Default**: `true`

If `true`, the picker will close when clicking anywhere outside of it.

### `hideOnEmojiSelect`

- **Type**: `boolean`
- **Default**: `true`

If `true`, the picker will automatically close when an emoji is selected.

### `hideOnEscape`

- **Type**: `boolean`
- **Default**: `true`

If `true`, the picker will close when the Escape key is pressed.

### `onPositionLost`

- **Type** [`PositionLostStrategy`](./position-lost-strategy)
- **Default**: `none`

Determines how to react when the picker loses its reference element. This typically happens when the reference element is removed from the DOM or is hidden with `display: none`. In either case, the picker loses its relative position (by default). See [`PositionLostStrategy`](./position-lost-strategy) for details of the options.

### `position`

- **Type**: [`Position`](./position)
- **Default**: `'auto'`

The positioning method to use for the popup picker.

### `showCloseButton`
- **Default**: `true`

If `true`, the popup will have a Close button.

### `referenceElement`

- **Type**: `HTMLElement` | `undefined`

If using relative positioning, this defines the element that the picker is positioned relative to. This is required if using relative positioning, but can be omitted if using fixed positioning.

### `triggerElement`

- **Type**: `HTMLELement` | `undefined`

The interactive element (usually a button) that will trigger the popup picker.
