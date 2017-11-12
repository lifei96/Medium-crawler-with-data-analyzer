function draw_SCC()
    Y = [838021, 23, 9, 7, 7, 7, 6, 6, 6, 6];
    X = {'1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'};
    bar(Y, 0.6, 'k');
    xlim([0.5 10.5])
    set(gca,'YScale','log')
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('Top 10 Strongly Connected Components','FontSize',20);
    ylabel('Component Size','FontSize',20);
    title('');
    grid off;
    print('./results/graph/SCC.eps', '-depsc')
end