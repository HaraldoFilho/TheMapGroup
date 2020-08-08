#!/usr/bin/perl

system "ls -d */ > members";

open MEMBERS_FILE, "members" or die "Can't open members file to read!\n";
my @members_lines = <MEMBERS_FILE>;
close MEMBERS_FILE;

foreach (@members_lines) {
    s/\/\n//;
    system "setup-member.sh $_";
    print "reseted member: $_\n"
}

system "rm members"
