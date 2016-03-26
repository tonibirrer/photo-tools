# photo-tools
A few handy tools I maintain to handle my photo library

## Prune

When I take pictures, both RAW (CR2) and JPG files
are written into the same folder.

I then review the JPGs (because its faster) and manually delete the ones I don't like.

This tool helps me to automatically identify the deleted JPGs and find the relating CR2 and prunes these too.

The tool never deletes file, without the --force switch
Your photos are precious ;-)


### Examples

#### Scan for files in the current folder (dry run)
```
./prune.py
```
#### Scan for files in the current folder, and delete obsolete RAW files

```
./prune.py --force
```

#### Scan for files in a different folder (dry run)

```
./prune.py --folder /my/folder/with/photos
```

### Caveats
I've only tested this on OSX.
