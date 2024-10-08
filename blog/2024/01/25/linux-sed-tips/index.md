---
slug: linux-sed-tips
title: Search and replace (or add) using sed
authors: [christophe]
image: /img/bash_tips_social_media.jpg
tags: [.env, bash, linux, sed, tips]
enableComments: true
---
![Search and replace (or add) using sed](/img/bash_tips_banner.jpg)

Today, I was facing (once more) with the following need: I need to update a setting in a text file but if the variable is not yet present, I need to add it.

So, in short, I need to make a *search and replace or insert new line*.

Using `sed` it's quite easy to automate the search & replace but how to append?

<!-- truncate -->

This article will explains one-way to achieve this. You'll find a lot of other possibilities on Internet and some only using the `sed` instruction but ... can you read them?

I prefer to use a different approach, perhaps not the *native one* but, yeah, I can read it.

## Search and replace

Imagine a `.env` file with just one line, like f.i.:

```bash
echo 'APP_ENV = local' > .env
```

I can update `APP_ENV` f.i. using:

```bash
sed -i "s/APP_ENV =.*/APP_ENV = production/" .env
```

Easy no? The `s` in the command is for `substitute` (replace) and the used delimiter is `/`. So, `sed` will search for `APP_ENV =.*` and if found, will replace with `APP_ENV = production`. The `-i` flag means that the new content (after replacement) has to be rewritten in the file.

## Don't replace but add if not found

But what if `APP_ENV` is not present at all in the file?

Of course, by running `sed -i "s/APP_ENV =.*/APP_ENV = production/" .env` nothing will happens (you can verify with `cat .env`).

Before seeing how to do, run the following block and you'll get a `NOT FOUND` message.

```bash
echo 'APP_NAME = My application' > .env
grep -q "^APP_ENV =" .env && echo "FOUND" || echo "NOT FOUND"
```

So if `grep -q` is successful (we've retrieved `APP_ENV` in the file) then we continue (`&&`) and display `FOUND` otherwise (`||`) we'll display `NOT FOUND`.

`&&` means that the previous command is successful (i.e. has been retrieved by `grep`) and `||` means not successful (not retrieved).

So, the next example will now display `FOUND`.

```bash
echo 'APP_NAME = My application' > .env
echo 'APP_ENV = local' >> .env
grep -q "^APP_ENV =" .env && echo "FOUND" || echo "NOT FOUND"
```

## Combine both

Ok, first we can make our replace statement:

```bash
echo 'APP_NAME = My application' > .env
echo 'APP_ENV = local' >> .env

grep -q "^APP_ENV =" .env \
    && sed -i "s/APP_ENV =.*/APP_ENV = production/" .env \
    || echo "NOT FOUND"
```

By running `cat .env`, you will get, as expected, `APP_ENV = production`.

And the next block will still display `NOT FOUND`:

```bash
echo 'APP_NAME = My application' > .env

grep -q "^APP_ENV =" .env \
    && sed -i "s/APP_ENV =.*/APP_ENV = production/" .env \
    || echo "NOT FOUND"
```

The *insert a new line* command is this one: `sed -i -e '$aAPP_ENV = production' .env`. The `-e` argument allow to execute a script and it's quite strange but the script is `$a`. That command is for *append line*. And now you've understood that sed will here add a new line in the file.

## The final instruction

Here it's:

```bash
echo 'APP_NAME = My application' > .env

grep -q "^APP_ENV =" .env \
    && sed -i "s/APP_ENV =.*/APP_ENV = production/" .env \
    || sed -i -e '$aAPP_ENV = production' .env
```

Finally, by running `cat .env` we can see the result:

```text
APP_NAME = My application
APP_ENV = production
```
