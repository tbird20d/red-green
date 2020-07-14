test:
	./test.sh

clean:
	rm -f rgdata/rgdata*
	rm -f rgdata/winners*
	rm -rf rgdata/rps-r*
	rm -rf rgdata/trivia-q*
	rm -f rgdata/still_in/*
	rm -f rgdata/still_in_backup/*
	@echo "*** NOTE: rgdata/users was not erased ***"
