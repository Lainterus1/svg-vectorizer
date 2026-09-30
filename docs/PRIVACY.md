# SVG Vectorizer privacy policy

Updated: September 30, 2026
Publisher: **Daniil** ([Lainterus1 on GitHub](https://github.com/Lainterus1))
Support and privacy contact: **gonchardaniil1998@gmail.com**

This policy describes SVG Vectorizer's local implementation. It is separate from
the policies of ChatGPT/Codex, Gmail and other services you choose to use.

## Local image processing

The plugin reads the PNG, JPEG or WebP image you select and the conversion options
you provide. An image may contain personal data. The plugin does not need an account,
API key, contact list or information about the image's owner. Only process images
you have the right to use.

The purpose is to decode the raster, generate an SVG and validate its rendering.
The CLI does not send your images, SVGs or conversion options to external services.
Python and Node communicate locally through standard input/output. Dependency
installation makes ordinary installer requests to PyPI/npm and their infrastructure.

If you upload a file to ChatGPT/Codex or ask another service to share the result,
that platform and the recipient process it under their own rules. Those actions
are outside the standalone CLI.

## Files and retention

The input stays unchanged. The output SVG remains at the path you choose until you
delete it. A successful conversion replaces an existing output only after validation;
it does not keep a backup of the previous successful result.

A temporary SVG is removed after replacement or a handled error. An operating-system
or process crash may leave a `.vectorize-*.svg` file beside the output. The plugin
has no persistent database, telemetry or background service. Console messages can
contain file paths and may be retained by your terminal or agent under its settings.

You control the input and destination, can cancel a conversion, and can delete its
outputs and leftover temporary files.

## Support correspondence

When you voluntarily contact support, the publisher receives your email address,
message and attachments to answer your request. Correspondence is handled in Gmail
and is accessible to the publisher. Do not attach an image if a text explanation is
enough. Do not send passwords, API keys, government identifiers, payment information
or medical records; use an anonymized sample when an example is necessary.

The publisher deletes support correspondence within **30 days after an issue is
closed**, or earlier at the sender's request. Send deletion requests to the contact
address above. This is the publisher's support-handling policy; the CLI does not
manage the mailbox or automatically delete messages.

Local CLI processing does not imply that a platform through which you upload files
or contact support performs no data processing. Those platforms' own policies also apply.
