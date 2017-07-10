function draw_Modularity()
    Y = [0.456409, 0.456173, 0.447369, 0.456406, 0.444644, 0.439527, 0.426931, 0.422556, 0.417061, 0.423531];
    X = {'10^{-6}', '10^{-5}', '10^{-4}', '10^{-3}', '10^{-2}', '10^{-1}', '0.2', '0.3', '0.4', '0.5'};
    bar(Y, 0.6, 'k');
    xlim([0.5 10.5])
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    xlabel('\delta', 'FontSize', 20);
    ylabel('Modularity','FontSize',20);
    title('');
    grid off;
    print('./results/graph/Modularity.eps', '-depsc')
end