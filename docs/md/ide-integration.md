# IDE Integration

You can integrate `quikrun` with your favorite editors and IDEs to execute your scripts with a single keybinding (e.g., `Ctrl+Alt+N`).

Here are setup instructions for several popular editors:

## Zed

You can define a project-level or global task in Zed to run the current active file using `quikrun`.

#### Define the Task

Create or edit your `.zed/tasks.json` in your project root (or open your global tasks via `zed: open tasks` from command palette):

```json
[
  {
    "label": "Run Current File",
    "command": "quikrun '${ZED_FILE}'",
    "save": "current",
    "use_new_terminal": false,
    "allow_concurrent_runs": true,
    "reveal": "always"
  }
]
```

For explanations of these options, refer to the [Zed Tasks Docs](https://zed.dev/docs/tasks).

#### Bind a Key

To run the task with a keyboard shortcut (e.g., `Ctrl+Alt+N`):

Create or edit `.zed/keymap.json` in your project root (or run `zed: open keymap` from the command palette) and add:

```json
[
  {
    "context": "Editor && mode == full && vim_mode == normal", // Adjust context as needed
    "bindings": {
      "ctrl-alt-n": ["task::Spawn", { "task_name": "Run Current File" }]
    }
  }
]
```

Learn more about contexts [here](https://zed.dev/docs/key-bindings?highlight=keymap#contexts)

## VS Code (& it's derivatives)

You can configure VS Code tasks to run the currently focused file.

#### Create a Task

- Open the Command Palette (**Ctrl+Shift+P** / **Cmd+Shift+P**).
- Select **Tasks: Configure Task** → **Create tasks.json file from template**.
- Replace the file contents with the following configuration:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Current File",
      "type": "shell",
      "command": "quikrun",
      "args": ["${file}"],
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "shared",
        "showReuseMessage": false,
        "focus": true
      },
      "problemMatcher": []
    }
  ]
}
```

#### Configure Keyboard Shortcut

Open your global `keybindings.json` (via the command palette: `Preferences: Open Keyboard Shortcuts (JSON)`) and bind a shortcut to the task:

```json
[
  {
    "key": "ctrl+alt+n",
    "command": "workbench.action.tasks.runTask",
    "args": "Run Current File"
  }
]
```

## JetBrains IDEs (PyCharm, IntelliJ, WebStorm, CLion, etc.)

You can configure `quikrun` as an **External Tool** inside JetBrains IDEs, which allows you to run it on any active file and bind a keyboard shortcut to it.

#### Add Quikrun as an External Tool

1. Open settings (**Ctrl+Alt+S** / **Cmd+,**).
2. Navigate to **Tools** → **External Tools**.
3. Click the **+** (Add) icon.
4. Fill in the fields:
   - **Name**: `Quikrun`
   - **Program**: `quikrun` _(or the path to your `quikrun` executable if it is not in your global PATH)_
   - **Arguments**: `"$FilePath$"`
   - **Working directory**: `$ProjectFileDir$`
5. Click **OK** to save.

#### Assign a Keybinding

1. Still in settings, navigate to **Keymap**.
2. Search for `Quikrun` in the search bar.
3. Under **External Tools** → **External Tools**, right-click **Quikrun** and choose **Add Keyboard Shortcut**.
4. Press your desired shortcut (e.g., `Ctrl+Alt+N`) and click **OK**.

## Neovim / Vim

You can run `quikrun` directly within Vim's built-in terminal emulator.

### Lua (Neovim `init.lua`)

Add the following keymap to write the current file and execute `quikrun` inside a vertical/horizontal terminal split:

```lua
-- Save and run current file with quikrun in a horizontal terminal split
vim.keymap.set('n', '<C-A-n>', function()
  vim.cmd('write')
  vim.cmd('split | term quikrun ' .. vim.fn.shellescape(vim.fn.expand('%:p')))
end, { desc = 'Run Current File' })
```

### Vimscript (`.vimrc` or `init.vim`)

```vim
" Save and run current file in a horizontal split terminal
nnoremap <C-A-n> :w<CR>:split term://quikrun %:S<CR>

```

## Sublime Text

Create a custom Sublime Build System to compile/run files using `quikrun`.

1. Go to **Tools → Build System → New Build System...**
2. Paste the following configuration:

```json
{
  "cmd": ["quikrun", "$file"],
  "selector": "source",
  "working_dir": "$file_path",
  "shell": true
}
```

3. Save the file as `quikrun.sublime-build` in your default user packages folder.
4. Select `quikrun` from the Build System menu and run with `Ctrl+B` (or `Cmd+B` on macOS).
