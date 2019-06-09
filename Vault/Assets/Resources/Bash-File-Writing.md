To overwrite an existing file (or write to a new file) that you own, substituting variable references inside the heredoc:

cat << EOF > /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, with the variable contents substituted.
EOF

To append an existing file (or write to a new file) that you own, substituting variable references inside the heredoc:

cat << FOE >> /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, with the variable contents substituted.
FOE

To overwrite an existing file (or write to a new file) that you own, with the literal contents of the heredoc:

cat << 'END_OF_FILE' > /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, without the variable contents substituted.
END_OF_FILE

To append an existing file (or write to a new file) that you own, with the literal contents of the heredoc:

cat << 'eof' >> /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, without the variable contents substituted.
eof

To overwrite an existing file (or write to a new file) owned by root, substituting variable references inside the heredoc:

cat << until_it_ends | sudo tee /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, with the variable contents substituted.
until_it_ends

To append an existing file (or write to a new file) owned by user=foo, with the literal contents of the heredoc:

cat << 'Screw_you_Foo' | sudo -u foo tee -a /path/to/your/file
This line will write to the file.
${THIS} will also write to the file, without the variable contents substituted.
Screw_you_Foo

run as sudo:
sudo bash -c 'cat << EOF > /etc/yum.repos.d/some-name.repo
line1
line2
line3
EOF'