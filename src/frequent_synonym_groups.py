
import argh


@argh.arg('--synonyms', help='Number of synonyms', type=str, required=True)
def main(**kwargs):
    print 'hhh'
    print int(kwargs['synonyms'])

if __name__ == '__main__':
    parser = argh.ArghParser()
    parser.set_default_command(main)
    parser.dispatch()
